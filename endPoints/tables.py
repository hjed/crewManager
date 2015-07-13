"""
The file stores functions for table related endpoints in the Crew Manger API
Created: 2/06/2015
Aurthor: Harry J.E Day
"""

import logic.Users as Users
import logic.tables as tables
import logic.errorCodes as errorCodes

import endPoints.users as userEndpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb

import logging

class TableLinkResponse(messages.Message):
    #The name of the table
    tableName = messages.StringField(1,required=True)
    #the key of the table
    tableKey = messages.StringField(2, required=True)


#A response listing the tables a user has
class TableListResponse(messages.Message):
    #The key of the user this list is for
    userKey = messages.StringField(1, required=False)
    #The list of tables
    tables = messages.MessageField(TableLinkResponse,2,repeated=True)
    #the status 
    status = messages.IntegerField(3,required=True)

#a class requesting a table
class TableRequest(messages.Message):
    #the users token
    tokenKey = messages.StringField(1, required=True)
    #the table's table's key
    tableKey = messages.StringField(2, required=True)

class SIS10DataResponse(messages.Message):
    #leave the first 10 free for tabledata
    abseiling = messages.StringField(10)
    caving = messages.StringField(11)
    canyoning = messages.StringField(12)
    rockclimbing = messages.StringField(13)
    """
    Water
    """
    canoeing = messages.StringField(14)
    """
    Bushwalking
    """
    #these ones are weird
    bushwalking = messages.StringField(15)
    bushwalkingGuide = messages.StringField(16)
    """
    Common Core, etc
    """
    commonCoreAB1 = messages.BooleanField(17,required=True)
    trainATrainer = messages.BooleanField(18, required=True)
    firstAid = messages.StringField(19)
    """
    Cert of Buisness
    """
    eLearning = messages.BooleanField(20,required=True)
    eLearningAdvanced = messages.BooleanField(21,required=True)
    BPS = messages.BooleanField(22, required=True)
    Woodbeads = messages.BooleanField(23,required=True)


#A class representing a table
class SIS10TableResponse(messages.Message):
    #the status of the request
    status = messages.IntegerField(1, required=True)
    #The name of the table
    tableName = messages.StringField(2,required=False)
    #The key of the user this list is for
    userKey = messages.StringField(3, required=False)
    #the data of the table
    data = messages.MessageField(SIS10DataResponse,4,required=False)




class api():

    @staticmethod
    def listUserTables(request):
        resp = TableListResponse(status=1)
        (resp.status, user) = Users.User.authUser(ndb.Key(urlsafe=request.token))
        if resp.status == 0:
            resp.userKey = user.key.urlsafe()
            for tableLink in user.tables:
                resp.tables.append(TableLinkResponse(tableName=tableLink.tableName,tableKey=tableLink.link.urlsafe()))
        return resp
    
    @staticmethod
    def getSISTable(req):
        resp = SIS10TableResponse(status=1)
        logging.info(str(resp))
        (resp.status, user) = Users.User.authUser(ndb.Key(urlsafe=req.tokenKey))
        if resp.status == 0:
            logging.info(str(resp))
            resp.status = 1
            resp.userKey = user.key.urlsafe()
            tableKey = ndb.Key(urlsafe=req.tableKey)
            if tableKey is not None:
                logging.info(str(resp))
                table = tableKey.get()
                if table.hasReadPermision(user):
                    logging.info(str(resp))
                    if table is not None:
                        logging.info(str(resp))
                        resp.tableName = table.__class__.__name__
                        resp.data = SIS10DataResponse(
                            abseiling = table.abseiling,
                            caving = table.caving,
                            canyoning = table.canyoning,
                            rockclimbing = table.rockclimbing,
                            canoeing = table.canoeing,
                            #these ones are weird
                            bushwalking = table.bushwalking,
                            bushwalkingGuide = table.bushwalkingGuide,
                            commonCoreAB1 = table.commonCoreAB1,
                            trainATrainer = table.trainATrainer,
                            firstAid = table.firstAid,
                            eLearning = table.eLearning,
                            eLearningAdvanced = table.eLearningAdvanced,
                            BPS = table.BPS,
                            Woodbeads = table.Woodbeads,
                        )
                        resp.status =0
                    else:
                        resp.status =2 
                else:
                    resp.status = 21 #read permision denied
            else:
                resp.status = 2
        return resp