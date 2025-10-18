import unittest
import requests
import uuid
import os



class ServerTests(unittest.TestCase):
    session = requests.Session()

    def login_buyer(self):
        self.login_role("buyer")

    def login_realtor(self):
        self.login_role("realtor")


    def login_admin(self):
        self.login_role("admin")


    def login_role(self, role: str):
        url = f"{self.url}/api/user"
        payload_register = {
           "name": "My name " + str(uuid.uuid4()),
           "email": "myem" + str(uuid.uuid4()) + "ail@mail.com",
           "password": "hetryi459865ruhyrkjt86",
           "role": role,
           "status": "active"
        }
        requests.post(f"{url}/register", json=payload_register)
        payload_login = {
            "email": payload_register.get("email"),
            "password": payload_register.get("password")
        }
        self.session.post(f"{url}/login", json=payload_login)



    def setUp(self):
        self.url = os.getenv("TARGET_URL", "http://localhost:5000/")

    def test_post_get_realty(self):
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
        print("Response:", response.json())
        print(type(response))
        print("Status:", response.status_code)
        self.assertEqual(response.status_code, 201)

        response = requests.get(f"{url}/{response.json()["id"]}")
        print("Response: ", response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("Data: ", data)
        print("Data type: ", type(data))
        found = payload["title"] == data.get("title")
        self.assertTrue(found, f"Response does not contain item with title {payload['title']}")

    def test_delete_realty(self):
        url = f"{self.url}/api/realty/"
        payload = {
           "title": "My new realty",
           "price": 1000000,
           "city": "Toronto",
           "address": "address",
           "image": "image",
        }
        response = requests.post(url, json=payload)

        realty_id = response.json()["id"]
        print(realty_id)
        response = requests.delete(f"{url}{realty_id}")
        self.assertEqual(response.status_code, 200)
    
    def test_update_realty(self):
        url = f"{self.url}/api/realty/"
        payload_post = {
           "title": "My new realty",
           "price": 1000000,
           "city": "Toronto",
           "address": "address",
           "image": "image",
        }
        response = requests.post(url, json=payload_post)
        self.assertEqual(response.status_code, 201)
        realty_id = response.json().get("id")
        self.assertIsNotNone(realty_id)

        payload_update = {
           "id": realty_id,
           "title": "Updated title",
           "price": 44355,
           "city": "New city",
           "address": "New address",
           "image": "image",
        }
        response_update = requests.put(f"{url}{realty_id}", json=payload_update)
        self.assertEqual(response_update.status_code, 200, f"{response_update.json()}")
        check_response = requests.get(f"{url}{realty_id}").json()
        print(f"Updated data: {check_response}")
        self.assertEqual(check_response["title"], "Updated title")
        self.assertEqual(check_response["price"], 44355)

#user
    def test_update_user(self):
        
        self.login_buyer()
        
        payload = {
            "name": f"My name + {str(uuid.uuid4())}", 
            "email": f"myEmail_{str(uuid.uuid4())}", 
            "password": "mypassword"
        }

        resp = self.session.put(f"{self.url}/api/user/profile", json=payload)
        if resp.status_code >= 400:
            print(resp.status_code, resp.text)
            
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        print("Data: ", data)




    def test_login_user(self):
        self.login_buyer()
        resp = self.session.get(f"{self.url}/api/user/profile").json()
        print("Get profile:", resp)
        self.assertTrue(len(resp["name"]) > 5)


    def test_delete_user(self):
            url = f"{self.url}/api/user/"
            payload = {
           "name": "My name " + str(uuid.uuid4()),
           "email": "myem" + str(uuid.uuid4()) + "ail@mail.com",
            "password": "hetryi459865ruhyrkjt86",
            "reg_date": "10.15.2025.11:00AM",
            "role": "user",
            "status": "active"
            }
            response = requests.post(f"{url}/register", json=payload)

            user_id = response.json()["id"]
            print(user_id)
            print(type(user_id))
            print(f"{url}{user_id}")
            response = requests.delete(f"{url}{user_id}")
            self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()
