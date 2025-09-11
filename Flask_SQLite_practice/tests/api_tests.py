import unittest
import requests

class ServerTests(unittest.TestCase):
    def setUp(self):
        pass

    def testRegisterUser(self):
        url = "http://127.0.0.1:5000/"
        payload = {
            "title": "My title",
            "price": "1",
            "city": "My city"
        }
        response = requests.post(url, json=payload)

        print("Status:", response.status_code)
        print("Response:", response)
        pass

if __name__ == '__main__':

    unittest.main()
