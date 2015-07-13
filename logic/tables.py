"""
This file holds classes to store user 'tables' such as SIS10 quals or badge achivements
Date Created: 7/06/2015
Aurthor: Harry J.E Day <harry@dayfamilyweb.com>
"""


from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from google.appengine.ext.db import BadValueError

import datetime
import logging


class TableLink(ndb.Model):
    #The class name of the table
    tableName = ndb.StringProperty(indexed=False)
    #The key of the table object
    link = ndb.KeyProperty(kind='Table',required=True,indexed=False)
    
    """
    Class Methods
    """
    
    #safely retrives the table object returning relevant status codes
    #returns (status, table)
    #   status - the status code
    #   table - the table object or none on failure
    #post-condition: if the status is 0, the table object is not None
    def doSafeRetreval(self):
        if self.link is not None:
            table = self.link.get()
            if table is not None:
                return (0, table)
            else:
                return (2, None)
        else:
            return (4, None)
    
    
class Table(polymodel.PolyModel):
    #The user this table belongs to
    user = ndb.KeyProperty(kind='User',required=True,indexed=True)
    
    #attaches a table to a user, should be called by a subclass
    #The user and table must have already been created and put
    #Inputs
    #   - user - the user entity to attach this table to
    #Returns
    #   - status - the status code, 0 for success
    def attachTable(self,user):
        user.tables.append(TableLink(link=self.key, tableName=self.__class__.__name__))
        user.put()
        
    #Checks that the given user entity has read permsion on this table
    #Inputs
    #   user - the user
    #Returns
    #   true - if the user has permision, otherwise false
    def hasReadPermision(self,user):
        #TODO
        return True
    

#Most SIS10 Properties have a default set of values
#So this class implements a special class to store these
class SIS10Property(ndb.StringProperty):

    #confirms that the value is valid
    def _validate(self,value):
        if not isinstance(value, str) and value != "":
            raise TypeError('Excpected an string value, got %s' %repr(value))
        elif value not in ["Level 1", "Level 2", "Level 3", "Guide", "Instructor",""]:
            raise BadValueError("Expected " + str(["Level 1", "Level 2", "Level 3", "Guide", "Instructor"]))

#A table representing SIS10 qualifications
class SIS10Table(Table):
    """
    Rockcraft
    """
    abseiling = SIS10Property(required=True,default="")
    caving = SIS10Property(required=True,default="")
    canyoning = SIS10Property(required=True,default="")
    rockclimbing = SIS10Property(required=True,default="")
    """
    Water
    """
    canoeing = SIS10Property(required=True,default="")
    """s
    Bushwalking
    """
    #these ones are weird
    bushwalking = ndb.StringProperty(choices=set(["Level 1","Level 2","Level 3","Alpine",""]),default="")
    bushwalkingGuide = ndb.StringProperty(choices=set(["Level 1","Level 2","Level 3","Alpine",""]),default="")
    """
    Common Core, etc
    """
    commonCoreAB1 = ndb.BooleanProperty(default=False,required=True)
    trainATrainer = ndb.BooleanProperty(default=False, required=True)
    firstAid = ndb.StringProperty(choices=set(["Apply","Advanced","Remote",""]),default="")
    """
    Cert of Buisness
    """
    eLearning = ndb.BooleanProperty(default=False,required=True)
    eLearningAdvanced = ndb.BooleanProperty(default=False,required=True)
    BPS = ndb.BooleanProperty(default=False, required=True)
    Woodbeads = ndb.BooleanProperty(default=False,required=True)
    