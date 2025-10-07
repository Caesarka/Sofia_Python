import unittest
import requests
import uuid
import os

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.url = os.getenv("TARGET_URL", "http://localhost:5000/")
        pass

    def testPostRealty(self):
        guid = uuid.uuid4()
        url = f"{self.url}/api/realty/"
        payload = {
           "title": "My title " + str(guid),
           "price": 1,
           "city": "My city",
           "address": "address"
        }
        response = requests.post(url, json=payload)
        print("Response:", response.text)
        print("Status:", response.status_code)
        self.assertEqual(response.status_code, 201)

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        found = any(payload["title"] == item.get("title") for item in data)
        self.assertTrue(found, f"Response does not contain item with title {payload['title']}")

if __name__ == '__main__':
    unittest.main()
