var app = angular.module('crewManager', []); 
app.controller("pageLoad", ['$scope','$rootScope','$window', function($scope,$rootScope,$window) {
    $scope.currentPage = "login.html";
    //stores if the backend is ready to go
    $scope.ready = false;
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
        console.log("do Login")
        request = {
            "email": email,
            "password": password
        };
        console.log(request)
        gapi.client.crewManagerApi.users.login(request).execute(function(resp) {
            console.log(email)
            //login failed
            if (resp.status != 0) {
                console.log("failure")
                $scope.hasError = true;
                $scope.errorCode = resp.status;
                $scope.errorMessage = resp.errorMessage;
                
            } else {
               //clear error message on success
                $scope.hasError = false;
            }
            console.log(resp)
            //apply changes
            $scope.$apply();
        });
    };
}]);


function init() {
    window.init();
}