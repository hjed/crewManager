"""
This File Contains the Endpoint API Calls, which are then passed to other applications
Created: 2/06/2015
Aurthor: Harry J.E Day <harry@dayfamilyweb.com>
"""
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

import endPoints.users as users
import endPoints.tables as tables

@endpoints.api(name="crewManagerApi", version="v0.1", description="The Crew Manager Core API")
class CrewManagerApi(remote.Service):
    
    @endpoints.method(users.LoginRequest, users.LoginResponse,
                  path='users/login', http_method='POST',
                  name='users.login')
    def doLogin(self, request):
        return users.api.doLogin(request)
    
    #used to retive basic user info
    @endpoints.method(users.GetUserRequest, users.GetUserResponse,
                  path='users/getUser', http_method='POST',
                  name='users.getUser')
    def getUser(self, request):
        return users.api.getUser(request)
    
    #used to retive basic user info
    @endpoints.method(users.GetUserRequest, tables.TableListResponse,
                  path='tables/listUserTables', http_method='POST',
                  name='tables.listUserTables')
    def listUserTables(self, request):
        return tables.api.listUserTables(request)

app = endpoints.api_server([CrewManagerApi])
