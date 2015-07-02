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

@endpoints.api(name="crewManagerApi", version="v0.1", description="The Crew Manager Core API")
class CrewManagerApi(remote.Service):
    
    @endpoints.method(users.LoginRequest, users.LoginResponse,
                  path='crewManagerApi/login', http_method='POST',
                  name='crewManagerApi.Login')
    def doLogin(self, request):
        return users.api.doLogin(request)

app = endpoints.api_server([CrewManagerApi])
