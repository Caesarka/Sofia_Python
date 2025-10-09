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
           "address": "address",
           "image": "image",
        }
        response = requests.post(url, json=payload)
        print("Response:", response.text)
        print("Status:", response.status_code)
        self.assertEqual(response.status_code, 201)

        response = requests.get(url)
        print("Response: ", response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("Data: ", data)
        print("Data type: ", type(data))
        found = any(payload["title"] == item.get("title") for item in data)
        self.assertTrue(found, f"Response does not contain item with title {payload['title']}")

    def testGetRealty(self):
        url = f"{self.url}/api/realty/?id=30"
        response = requests.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["title"], "Townhouse")

    

if __name__ == '__main__':
    unittest.main()
