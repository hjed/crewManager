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

class Table(polymodel.PolyModel):
    #The user this table belongs to
    user = ndb.Key(kind='User',required=True,indexed=True)


class TableLink(ndb.Model):
    #The class name of the table
    tableName = ndb.StringProperty(indexed=False)
    #The key of the table object
    link = ndb.KeyProperty(kind=Table,required=True,indexed=False)
    
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
    

#Most SIS10 Properties have a default set of values
#So this class implements a special class to store these
class SIS10Property(ndb.StringProperty):

    #confirms that the value is valid
    def _validate(self,value):
        if not isinstance(value, str):
            raise TypeError('Excpected an string value, got %s' %repr(value))
        elif value not in ["Level 1", "Level 2", "Level 3", "Guide", "Instructor",None]:
            raise BadValueError("Expected " + str(["Level 1", "Level 2", "Level 3", "Guide", "Instructor"]))

#A table representing SIS10 qualifications
class SIS10Table(Table):
    """
    Rockcraft
    """
    abseiling = SIS10Property()
    caving = SIS10Property()
    canyoning = SIS10Property()
    rockclimbing = SIS10Property()
    """
    Water
    """
    canoeing = SIS10Property()
    """
    Bushwalking
    """
    #these ones are weird
    bushwalking = ndb.StringProperty(choice=set(["Level 1","Level 2","Level 3","Alpine"]))
    bushwalkingGuide = ndb.StringProperty(choice=set(["Level 1","Level 2","Level 3","Alpine"]))
    """
    Common Core, etc
    """
    commonCoreAB = ndb.BooleanProperty(default=False,required=True)
    trainATrainer = ndb.BooleanProperty(default=False, required=True)
    firstAid = ndb.StringProperty(choice=set(["Apply","Advanced","Remote"]))
    """
    Cert of Buisness
    """
    eLearning = ndb.BooleanProperty(default=False,required=True)
    eLearningAdvanced = ndb.BooleanProperty(default=False,required=True)
    BPS = ndb.BooleanProperty(default=False, required=True)
    Woodbeads = ndb.BooleanProperty(default=False,required=True)
    