"""
This file holds classes to perform user management
Date Created: 23/05/2015
Aurthor: Harry J.E Day <harry@dayfamilyweb.com>
"""


from google.appengine.ext import ndb

import datetime
import logging

import Crypto.Random
from Crypto.Protocol import KDF
from google.appengine.ext import ndb

from logic.tables import TableLink

#A class for handeling authentication tokens
#The key of this token is basically used as a sesion token
#Because keys are guarented to be unique and somewhat random
#and we aren't using the name attribute, this is resonably 
#secure
class Token(ndb.Model):
    #The number of days tokens are valid for
    AUTH_TOKEN_VALID_FOR = 30
    
    #Stores the key of the user object this is attached to
    user = ndb.KeyProperty(kind='User',required=True)
    #Stores the creation date of this object. This allows us to
    #remove properties that are too old
    dateCreated = ndb.DateTimeProperty(auto_now_add=True, required=True)
    
    """
    This function converts this token into a user.
    WARNING: If the token has expired it deletes it.
    It returns a tuple (success, user)
        success - indicates if the token could be sucesfully retrived
        user    - the user object or None if not succesful
    """
    def getUser(self):
        success = False;
        user = None
        #check we are not expired
        print self.dateCreated + datetime.timedelta(days=Token.AUTH_TOKEN_VALID_FOR)
        print datetime.datetime.now()
        
        if (self.dateCreated + datetime.timedelta(days=Token.AUTH_TOKEN_VALID_FOR)) >= (datetime.datetime.now() ):
            #check we can retrive the user
            if self.user is not None:
                user = self.user.get()
                if user is not None:
                    success = True
                else:
                    logging.info("user is none")
            else:
                logging.info("self.user is none")
        else:
            logging.info("Token expired")
            self.key.delete()
        return (success, user)
            
#This class stores the secure parts of a user (Password hashes, etc)
#It is bassed on the tutorial at https://brianmhunt.github.io/articles/strong-crypto-python-passwords/
#Unfortunatly googles default auth classes either require google accounts or use SHA encryption
#This isn't really secure, so we have to implement KDF
class AuthDetails(ndb.Model):
    """
    Constants
    """
    #The max number of iterations
    ITERATIONS = 120000
    #Abitary itteration offset, stored outside of datastore
    ITER_OFFSET = -218
    #The Length of the key
    KEY_LENGTH = 32
    
    #pseudo-random stream for salts and iteration entropy
    _randf = None
    
    """
    DataStore
    """
    #The key generated from the password 
    key = ndb.BlobProperty(indexed=False, required=True)
    #The random salt for this key
    salt = ndb.BlobProperty(indexed=False, required=True)
    # The number of KDF iterations, starting from ITERATIONS_2013 plus or
    # minus a small random amount, and increasing in amount over time to
    # compensate for increasing computational power.
    iterations = ndb.IntegerProperty(indexed=False)
    
    #TODO: add extra security here
    
    
    """
    Class Functions
    """
    #To prevent leaks through the use of str()
    def __str__(self):
        return unicode(self).encode('utf-8')

    #To prevent leaks through the user of str
    def __unicode__(self):
        return "<AuthDetails>"
    
    #used to generated random data
    @property
    def randomStream(self):
        #if the streat has not been intilised yet
        if not self._randf:
            self._randf = Crypto.Random.new()
        return self._randf
    
    #used to generate the multiplier for the number of itterations we need
    #to keep the processing power for this sensible
    #It doubles every two years from 2015
    def _multiplier(self):
        start = datetime.datetime(2015,1,1)
        now = datetime.datetime.now()
        return 2 ** ((now-start).days / 715)
    
    #used to calculate the number of itterations to use
    def _iterations(self):
        #the base, which grows with computational power
        base_iters = int(self.ITERATIONS * self._multiplier())
        
        #this variation allows us to increase the key space for the whole attack
        #by varying the number of itterations by 7%
        entropy = int(
            self.randomStream.read(2).encode('hex'), 16
        ) % int(base_iters * 0.07)

        # Return a sensible number of iterations;
        return base_iters + entropy
    
    #Function used to generate a key from a password
    def _generateKey(self,pword):
        return KDF.PBKDF2(pword, self.salt, dkLen=self.KEY_LENGTH, count=self.iterations + self.ITER_OFFSET).encode('hex')
    
    #Sets the password
    def setPassword(self,password):
        self.iterations = self._iterations()
        #generate a salt
        self.salt = self.randomStream.read(32).encode('hex')
        #generate hash
        self.key = self._generateKey(password)
    
    #checks the password
    def verifyPword(self, pword):
        #if we don't have a password, fail
        if not self.key:
            return False
        #otherwise check if its the same 
        return self.key == self._generateKey(pword)

#Represents a User/Crew Member
class User(ndb.Model):
    """
    Identity/Basic Information Properties
    """
    #Stores the user's first name
    firstName = ndb.StringProperty(required=True)
    #Stores the user's last name
    lastName = ndb.StringProperty(required=True)
    #Stores the user's email
    email = ndb.StringProperty(required=True)
    #Stores the user's membership number
    membershipNumber = ndb.IntegerProperty(required=False)
    """
    Security Properties
    """
    auth = ndb.StructuredProperty(AuthDetails, indexed=False, required=True)
    """
    Other Data
    """
    #Stores links to each table related to this user
    tables = ndb.StructuredProperty(TableLink,repeated=True,indexed=False)
    
    #Creates a new user
    @staticmethod
    def newUser(email, password, firstName, lastName, membershipNumber=None):
        user = User(
            email=email,
            firstName=firstName,
            lastName=lastName,
            membershipNumber=membershipNumber
        )
        user.auth = AuthDetails()
        user.auth.setPassword(password)
        user.put()
        return user
    
    #Takes in a authToken's Key and converts it to a user object
    #Returns (status, user) where
    #   status - error code
    #   user - user object or None on failure
    #post-condition - if status is 0, user is not none
    @staticmethod
    def authUser(authTokenKey):
        status = 10
        user = None
        
        if authTokenKey:
            authToken = authTokenKey.get()
            #check the key was valid
            if authToken:
                (success, user) = authToken.getUser()
                if success and user is not None:
                    status = 0
                else:
                    status = 14
            else:
                status = 11 #Invalid Authtoken
        else:
            status = 11 #Invalid Authtoken
        
        return (status,user)
    
    #Takes in a users email and password
    #Returns (status, user) where
    #   status - error code
    #   user - user object or None on failure
    #   token - the token object or None on failure
    @staticmethod
    def login(email, password):
        status = 10
        user = None
        #assume one user per username
        userResults = User.query(User.email == email).fetch(1)
        if userResults and len(userResults) != 0:
            u = userResults[0]
            if u.auth:
                auth = u.auth
                if auth.verifyPword(password):
                    status = 0
                    user = u
                    token = Token(
                        user = user.key
                    )
                    token.put()
                    return (status, user, token)
                else:
                    status = 12
            else:
                status = 3
                
        else:
            status = 12 #Invalid user
        return (status, None, None)
        
        
    