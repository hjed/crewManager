import unittest

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util  # noqa

import logic.Users as users
import logic.tables as tables

import endPoints.users as userEndpoints
import endPoints.tables as tableEndpoints

import logging

class UserTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Initialize the datastore stub with this policy.
        self.testbed.init_datastore_v3_stub()
        # Initialize memcache stub too, since ndb also uses memcache
        self.testbed.init_memcache_stub()
        # Clear in-context cache before each test.
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def testUserCreation(self):
        user = users.User.newUser("test@test.com","pa$$W0rd","first","last")
        logging.info("testing return result")
        assert user != None
        assert user.key
        logging.info("testing get")
        assert user.key.get()
        logging.info("testing query")
        q = users.User.query(users.User.email == "test@test.com")
        self.assertEquals(1,q.count(5))
        res = q.fetch(1)
        self.assertEquals(1,len(res))
        self.assertEquals(user,res[0])
        self.assertEqual(res[0].email, "test@test.com")
        self.assertEqual(res[0].firstName, "first")
        
    def testUserCreation_MembershipNumber(self):
        user = users.User.newUser("test@test.com","pa$$W0rd","first","last",1234)
        logging.info("testing return result")
        assert user != None
        assert user.key
        logging.info("testing get")
        assert user.key.get()
        logging.info("testing query")
        q = users.User.query(users.User.email == "test@test.com")
        self.assertEquals(1,q.count(5))
        res = q.fetch(1)
        self.assertEquals(1,len(res))
        self.assertEquals(user,res[0])
        self.assertEqual(res[0].email, "test@test.com")
        self.assertEqual(res[0].firstName, "first")
        self.assertEqual(res[0].membershipNumber, 1234)
        
    def testUserLogin(self):
        user = users.User.newUser("test@test.com","pa$$W0rd","first","last",1234)
        logging.info("testing return result")
        assert user != None
        assert user.key
        logging.info("testing get")
        assert user.key.get()
        logging.info("testing query")
        q = users.User.query(users.User.email == "test@test.com")
        self.assertEquals(1,q.count(5))
        res = q.fetch(1)
        self.assertEquals(1,len(res))
        self.assertEquals(user,res[0])
        self.assertEqual(res[0].email, "test@test.com")
        self.assertEqual(res[0].firstName, "first")
        self.assertEqual(res[0].membershipNumber, 1234)
        (status, user, auth) = user.login("test@test.com","pa$$W0rd")
        assert user is not None
        assert auth is not None
        self.assertEqual(0,status)
        
    def testEndpointFunction_Login(self):
        user = users.User.newUser("test@test.com","pa$$W0rd","first","last",1234)
        logging.info("testing return result")
        assert user != None
        assert user.key
        logging.info("testing get")
        assert user.key.get()
        logging.info("testing query")
        q = users.User.query(users.User.email == "test@test.com")
        self.assertEquals(1,q.count(5))
        res = q.fetch(1)
        self.assertEquals(1,len(res))
        self.assertEquals(user,res[0])
        self.assertEqual(res[0].email, "test@test.com")
        self.assertEqual(res[0].firstName, "first")
        self.assertEqual(res[0].membershipNumber, 1234)
        
        req = userEndpoints.LoginRequest(email="test@test.com", password="pa$$W0rd")
        resp = userEndpoints.api.doLogin(req)
        
        self.assertEqual(0,resp.status)
        assert resp.tokenKey is not None
        
    def testEndpointFunction_TabeList(self):
        user = users.User.newUser("test@test.com","pa$$W0rd","first","last",1234)
        logging.info("testing return result")
        assert user != None
        assert user.key
        logging.info("testing get")
        assert user.key.get()
        logging.info("testing query")
        q = users.User.query(users.User.email == "test@test.com")
        self.assertEquals(1,q.count(5))
        res = q.fetch(1)
        
        table = tables.SIS10Table(user=res[0].key)
        table.put()
        table.attachTable(user)
        self.assertEquals(1,len(res))
        self.assertEquals(user,res[0])
        self.assertEqual(res[0].email, "test@test.com")
        self.assertEqual(res[0].firstName, "first")
        self.assertEqual(res[0].membershipNumber, 1234)
        
        req = userEndpoints.LoginRequest(email="test@test.com", password="pa$$W0rd")
        resp = userEndpoints.api.doLogin(req)
        
        self.assertEqual(0,resp.status)
        assert resp.tokenKey is not None
        req = userEndpoints.GetUserRequest(token=resp.tokenKey)
        resp = tableEndpoints.api.listUserTables(req)
        assert resp.status == 0
        assert resp.tables is not None
        assert resp.tables[0] is not None

       

        