//some constants

//TODO: load this from an api call
TABLE_NAMES = {"SIS10Table":"SIS10 Qualifications"}

SIS10_COL_TITLES = {
    "BPS": "BPS",
    "Woodbeads": "Wood Beads",
    "abseiling": "Abseiling",
    "bushwalking": "Bushwalking",
    "bushwalkingGuide": "Bushwalking Guide",
    "canoeing": "Canoeing",
    "canyoning": "Canyoning",
    "caving": "Caving",
    "commonCoreAB1": "Common Core A+B1",
    "eLearning": "E-Learning",
    "eLearningAdvanced": "Advanced E-Learning",
    "firstAid": "First Aid",
    "rockclimbing": "Rock Climbing",
    "trainATrainer": "Train A Trainer"
}

SIS10_COL_INPUT_TYPES = {
    "BPS": "checkbox",
    "Woodbeads": "checkbox",
    "abseiling": "select",
    "bushwalking": "select",
    "bushwalkingGuide": "select",
    "canoeing": "select",
    "canyoning": "select",
    "caving": "select",
    "commonCoreAB1": "checkbox",
    "eLearning": "checkbox",
    "eLearningAdvanced": "checkbox",
    "firstAid": "checkbox",
    "rockclimbing": "select",
    "trainATrainer": "checkbox"
}

//SIS10_DEFAULT_COL_OPTIONS = ["Level 1", "Level 2", "Guide", "Instructor", ""]
SIS10_DEFAULT_COL_OPTIONS = ["1", "2", "G", "I", ""]
SIS10_BWALK_COL_OPTIONS = ["Level 1", "Level 2", "Level 3", "Alpine", ""]
SIS10_OPTIONS = {
    "abseiling": SIS10_DEFAULT_COL_OPTIONS,
    "bushwalking": SIS10_BWALK_COL_OPTIONS,
    "bushwalkingGuide": SIS10_BWALK_COL_OPTIONS,
    "canoeing": SIS10_DEFAULT_COL_OPTIONS,
    "canyoning": SIS10_DEFAULT_COL_OPTIONS,
    "caving": SIS10_DEFAULT_COL_OPTIONS,
    "rockclimbing": SIS10_DEFAULT_COL_OPTIONS
}



var app = angular.module('crewManager', ['wt.responsive']); 
app.controller("pageLoad", ['$scope','$rootScope','$window', function($scope,$rootScope,$window) {
    $scope.currentPage = "login.html";
    //stores if the backend is ready to go
    $scope.ready = false;
    //stores if the user is logged in
    //NOTE: this should not be taken as correct without also checking the token
    $scope.loggedIn = true;
    //session token
    $scope.token = null;
    //user 
    $scope.user = null;
    
    //called to load the app
    $scope.startApp = function() {
        //load the cloud endpoints
        var ROOT = 'http://localhost:8080/_ah/api';
        gapi.client.load('crewManagerApi', 'v0.1', function() {
            $scope.ready = true;
            //needed because this runs in a different thread to angular
            $scope.$apply();
        }, ROOT);
    };
    
    //this allows angular and google endpoints to work together
    $window.init = function() {
        $scope.$apply($scope.startApp);
    };
    
    //handles succesfull logins
    $scope.loginSuccess = function(token) {
            console.log("logged in");
            $scope.token = token;
            $scope.loggedIn = true;
            $scope.currentPage = "home.html";
            //apply changes
            $scope.$apply();
            //load the user info
            request = {
                "token": $scope.token
            };
            console.log(request)
            gapi.client.crewManagerApi.users.getUser(request).execute(function(resp) {
                console.log(resp)
                //login failed
                if (resp.status != 0) {
                    //TODO: error message
                    
                } else {
                    $scope.user = resp.user
                }
                console.log(resp)
                //apply changes
                $scope.$apply();
            });
    }
}]);

app.controller("loginForm", ['$scope','$rootScope','$window', function($scope,$rootScope,$window) {
//     console.log($scope)
//     console.log($rootScope)
    //field variables
    $scope.email = "";
    $scope.password = "";
    //Error handeling
    $scope.hasError = false;
    $scope.errorMessage = "";
    $scope.errorCode = 0;
    //handles loging in
    $scope.doLogin = function(email,password) {
       
        request = {
            "email": email,
            "password": password
        };
        console.log(request)
        gapi.client.crewManagerApi.users.login(request).execute(function(resp) {
            console.log(email)
            //login failed
            if (resp.status != 0) {
                $scope.hasError = true;
                $scope.errorCode = resp.status;
                $scope.errorMessage = resp.errorMessage;
                
            } else {
               //clear error message on success
                $scope.hasError = false;
                $scope.$parent.loginSuccess(resp.tokenKey);
                
            }
            console.log(resp)
            //apply changes
            $scope.$apply();
        });
    };
}]);

app.controller("userTablesWidget", ['$scope','$rootScope','$window', function($scope,$rootScope,$window) {
    $scope.tables = [];
    
    $scope.loadTable = function(table) {
        req = {
                "tokenKey": $scope.$parent.token,
                "tableKey": table.tableKey
        }
        console.log(req)
        gapi.client.crewManagerApi.tables.getSISTable(req).execute(function(resp) { 
            console.log(resp)
            if (resp.status == 0) {

                table.data = [];
                for (var key in resp.data) {
                    tabl = {
                        "header":SIS10_COL_TITLES[key],
                        "value": resp.data[key],
                        "inputType": SIS10_COL_INPUT_TYPES[key],
                    }
                    if (tabl["inputType"] == "select") {
                        tabl["options"] = SIS10_OPTIONS[key]
                    }
                    table.data.push(tabl);
                }
                $scope.$apply();
            }
        });
    }
    
    //load the user's tables
    req = {"token": $scope.$parent.token};
    gapi.client.crewManagerApi.tables.listUserTables(req).execute(function(resp) { 
        console.log(resp)
        if (resp.status == 0) {
            $scope.tables = resp.tables
            $scope.tables.forEach(function(table) {
                table.name = TABLE_NAMES[table.tableName];
                $scope.loadTable(table);
            });
            $scope.$apply();
        }
    });
}]);

function init() {
    window.init();
}