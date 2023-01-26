try:
    import unittest

    from app import app 
except:
    print('Please try again!. some modules missing!')

class FlaskTest(unittest.TestCase):
    def testIndexSignin(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/signin',json={"email":"email@domain.com", "password":"somepassword"})
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
    def testIndexSigninData(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/signin',json={"email":"email@domain.com", "password":"somepassword"})
        self.assertTrue(b'message' in response.data or b'x-access-token' in response.data)
    def testIndexChpwd(self):
        tester = app.test_client(self)
        response = tester.put('/api/v1/changePassword',json= {
            "oldpassword":"newstrongpassword2",
            "newpassword":"newstrongpassword2",
            "confirmpassword":"newstrongpassword2" 
        })
        statuscode = response.status_code
        self.assertEqual(statuscode,200)

    def testIndexChpwdData(self):
        tester = app.test_client(self)
        response = tester.put('/api/v1/changePassword',json= {
            "oldpassword":"newstrongpassword2",
            "newpassword":"newstrongpassword2",
            "confirmpassword":"newstrongpassword2" 

        })
        self.assertTrue(b'message' in response.data or b'Alert' in response.data)
    def testIndexTodoGet(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/todos/',json= {})
        self.assertTrue(b'message' in response.data or b'Alert' in response.data)
    def testIndexTodoPost(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/todos',json= {})
        self.assertTrue(b'message' in response.data or b'Alert' in response.data)
    def testIndexTodoPut(self):
        tester = app.test_client(self)
        response = tester.put('/api/v1/todos',json= {})
        self.assertTrue(b'message' in response.data or b'Alert' in response.data)
    def testIndexTodoDelete(self):
        tester = app.test_client(self)
        response = tester.delete('/api/v1/todos',json= {})
        self.assertTrue(b'message' in response.data or b'Alert' in response.data)

if __name__ == '__main__':
    unittest.main()