import unittest
from jwksServer import app 

class TestAuthEndpoint(unittest.TestCase):

    def setUp(self): #Sets up Test Client
        self.app = app.test_client()
        self.username = "userABC"
        self.password = "password123"
        self.expired_query = "?expired=true"
        self.passed_tests = 0
        self.total_tests = 0

    def run_test(self, test_method): #Runs each test method
        self.total_tests += 1
        try:
            test_method()
            self.passed_tests += 1
        except AssertionError as e:
            print(f"Test failed: {test_method.__name__}\n{str(e)}")

    def test_successful_authentication(self): #Runs test for unexpired token
        data = {"username": self.username, "password": self.password}
        response = self.app.post('/auth', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def test_successful_authentication_with_expired_query(self): #Runs test for expired token
        data = {"username": self.username, "password": self.password}
        response = self.app.post('/auth' + self.expired_query, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def test_authentication_failure(self): #Runs test for invalid credentials
        data = {"username": "invalid_user", "password": "invalid_password"}
        response = self.app.post('/auth', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b'Authentication failed')

if __name__ == '__main__': #Checks flask app name
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthEndpoint) #Loads Test Suite
    test_runner = unittest.TextTestRunner(verbosity=2) #Runs Test Suite
    result = test_runner.run(test_suite)
    passed_percentage = (result.testsRun - len(result.errors) - len(result.failures)) / result.testsRun * 100 #Calculates percentage
    print(f"Passed {round(passed_percentage, 2)}% of test cases.") #Prints result

'''
 Use of ChatGPT in This Assignment
 I used ChatGPT to assist with coding the server as well as the test suite. I started off by asking ChatGPT to help create a JWKS server using flask. 
 From there I looked into how it encrypted the keys using RSA and changed the implementation method. After that I looked into how it made the JWKS
 Dictionary and rewrote the implementation for that. Then I asked ChatGPT how to create a "kid" and used the UUID method that it gave me. I then asked it how 
 to check if a JWKS key was expired before converting it to JSON. I implemented the method it gave me to check for expiration. Then I asked ChatGPT how
 to return both an expired and unexpired signed JWT on a POST request. I then added a way to check for expiration before sending out a signed JWT. Finally, 
 I asked ChatGPT to help create a test suite for my code, that would also give me a percentage of completion. I then made that code into the test suite file 
 I have. That's how I used ChatGPT during this assignment and the questions that I asked throughout to get to my goals.
'''
