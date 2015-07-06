"""
The file stores functions for user related endpoints in the Crew Manger API
Created: 2/06/2015
Aurthor: Harry J.E Day
"""

import logic.Users as Users
import logic.errorCodes as errorCodes

from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb

#Represents a request to login
class LoginRequest(messages.Message):
    #the email of the user trying to login
    email = messages.StringField(1,required=True)
    #the password of the user trying to login
    #this is sent under ssl, but in plaintext
    password = messages.StringField(2,required=True)

class LoginResponse(messages.Message):
    #the session key / token the user can use to authenticate their requests
    tokenKey = messages.StringField(1, required=False)
    #the status of the request
    status = messages.IntegerField(2, required=True)
    #the error message of the request (if the request fails)
    errorMessage = messages.StringField(3, required=False)
    
class GetUserRequest(messages.Message):
    #the token of this user
    token = messages.StringField(1, required=True)


class UserResponse(messages.Message):
    #Stores the user's first name
    firstName = messages.StringField(1,required=True)
    #Stores the user's last name
    lastName = messages.StringField(2,required=True)
    #Stores the user's email
    email = messages.StringField(3,required=True)
    #Stores the user's membership number
    membershipNumber = messages.IntegerField(4,required=False)


class GetUserResponse(messages.Message):
    #the status of the request
    status = messages.IntegerField(1, required=True)
    #the error message of the request (if the request fails)
    errorMessage = messages.StringField(2, required=False)
    #the user
    user = messages.MessageField(UserResponse,3)
    
class api():
    
    @staticmethod
    def doLogin(req):
        resp = LoginResponse(status = 1)
        
        (resp.status, user, token) = Users.User.login(req.email, req.password)
        if resp.status == 0:
            resp.tokenKey = token.key.urlsafe()
        else:
            resp.errorMessage = errorCodes.ERROR_CODES[resp.status]
        
        return resp
    
    @staticmethod
    def getUser(req):
        resp = GetUserResponse(status = 1)
        
        key = ndb.Key(urlsafe=req.token)
        if key:
            (resp.status, user) = Users.User.authUser(key)
            #we don't need to check user, because authUser checks
            if resp.status == 0:
                resp.user = UserResponse(
                    firstName = user.firstName,
                    lastName = user.lastName,
                    email = user.email,
                    membershipNumber = user.membershipNumber
                )
            else:
                resp.errorMessage = errorCodes.ERROR_CODES[resp.status]
        else:
            resp.status = 11 
            resp.errorMessage = errorCodes.ERROR_CODES[resp.status]
        
        return resp