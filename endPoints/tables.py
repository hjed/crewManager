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