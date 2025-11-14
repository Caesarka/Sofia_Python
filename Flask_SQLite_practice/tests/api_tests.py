import unittest
import requests
import uuid
import os

from schemas.realty_model import RealtyPatch



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
        self.login_realtor()
        resp = self.session.get(f"{self.url}api/user/profile").json()
        print("Get profile:", resp)

        guid = uuid.uuid4()
        url = f"{self.url}api/realty"
        payload = {
           "title": "My title " + str(guid),
           "price": 1,
           "city": "My city",
           "address": "address",
           "image": "image",
           "user_id": resp["id"]
        }

        response = self.session.post(url, json=payload)
        print("POST Response:", response.json())
        print("Status:", response.status_code)
        self.assertEqual(response.status_code, 201)

        data_post = response.json()
        self.assertIn("id", data_post, "Response JSON does not contain 'id' field")

        realty_id = data_post["id"]
        response = self.session.get(f"{url}/{realty_id}")
        print("GET Response: ", response.text)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        print("Data: ", data)

        self.assertEqual(payload["title"], data.get("title"), f"Expected title '{payload['title']}', got '{data.get('title')}'")


    def test_post_get_realty_buyer(self):
        self.login_realtor()
        resp = self.session.get(f"{self.url}api/user/profile").json()
        guid = uuid.uuid4()
        url = f"{self.url}api/realty"
        payload = {
           "title": "My title " + str(guid),
           "price": 1,
           "city": "My city",
           "address": "address",
           "image": "image",
           "user_id": resp["id"]
        }
        self.session.post(url, json=payload)

        self.login_buyer()
        resp = self.session.get(f"{self.url}api/user/profile").json()
        print("Get profile:", resp)

        guid = uuid.uuid4()
        url = f"{self.url}api/realty"
        payload = {
           "title": "My title " + str(guid),
           "price": 1,
           "city": "My city",
           "address": "address",
           "image": "image",
           "user_id": resp["id"]
        }

        response = self.session.post(url, json=payload)
        print("POST Response:", response.json())
        print("Status:", response.status_code)
        self.assertEqual(response.status_code, 403)

        response = self.session.get(f"{url}/")
        realties = response.json()
        print(realties)




    def test_delete_realty(self):
        self.login_realtor()
        resp = self.session.get(f"{self.url}/api/user/profile").json()
        print("Get profile:", resp)

        guid = uuid.uuid4()
        url = f"{self.url}/api/realty/"
        payload = {
           "title": "My title " + str(guid),
           "price": 1,
           "city": "My city",
           "address": "address",
           "image": "image",
           "user_id": resp["id"]
        }

        response = self.session.post(url, json=payload)

        data_post = response.json()
        realty_id = data_post["id"]

        response = self.session.delete(f"{url}{realty_id}")
        self.assertEqual(response.status_code, 200)
    
    def test_replace_realty(self):
        self.login_realtor()
        resp = self.session.get(f"{self.url}/api/user/profile").json()
        print("Get profile:", resp)

        guid = uuid.uuid4()
        url = f"{self.url}/api/realty/"
        payload = {
           "title": "My title " + str(guid),
           "price": 1,
           "city": "My city",
           "address": "address",
           "image": "image",
           "user_id": resp["id"]
        }

        response = self.session.post(url, json=payload)
        self.assertEqual(response.status_code, 201)

        data_post = response.json()
        realty_id = data_post["id"]

        payload["id"] = realty_id
        payload["title"] = "Updated title"
        payload["price"] = 44355

        response_replace = self.session.put(f"{url}{realty_id}", json=payload)
        print(response_replace)
        self.assertEqual(response_replace.status_code, 200, f"{response_replace.json()}")
        check_response = self.session.get(f"{url}{realty_id}").json()
        print(f"Updated data: {check_response}")
        self.assertEqual(check_response["title"], "Updated title")
        self.assertEqual(check_response["price"], 44355)

    def test_patch_realty(self):
        self.login_realtor()
        resp = self.session.get(f"{self.url}/api/user/profile").json()
        print("Get profile:", resp)

        guid = uuid.uuid4()
        url = f"{self.url}/api/realty/"
        payload = {
           "title": "My title " + str(guid),
           "price": 1,
           "city": "My city",
           "address": "address",
           "image": "image",
           "user_id": resp["id"]
        }

        response = self.session.post(url, json=payload)
        self.assertEqual(response.status_code, 201)

        data_post = response.json()
        realty_id = data_post["id"]

        realty_patch = RealtyPatch(title="Updated title", price=44355).model_dump()
        print(realty_patch)

        response_replace = self.session.patch(f"{url}{realty_id}", json=realty_patch)
        print(response_replace)
        self.assertEqual(response_replace.status_code, 200, f"{response_replace.json}")
        check_response = self.session.get(f"{url}{realty_id}").json()
        print(f"Updated data: {check_response}")
        self.assertEqual(check_response["title"], "Updated title")
        self.assertEqual(check_response["price"], 44355)

        self.login_admin()
        #resp = self.session.get(f"{self.url}/{realty_id}/publish").json()
        realty_patch = RealtyPatch().model_dump()
        print(realty_patch)
        response_publish = self.session.patch(f"{url}{realty_id}/publish", json=realty_patch)
        print(response_publish)
        self.assertEqual(response_publish.status_code, 200, f"{response_publish.json}")

    
    def test_buyer_add_realty(self):
        self.login_buyer()
        resp = self.session.get(f"{self.url}/api/user/profile").json()
        print("Get profile:", resp)
        guid = uuid.uuid4()
        url = f"{self.url}/api/realty/"
        payload = {
           "title": "My title " + str(guid),
           "price": 1,
           "city": "My city",
           "address": "address",
           "image": "image",
           "user_id": resp["id"]
        }

        response = self.session.post(url, json=payload)
        self.assertEqual(response.status_code, 403, f"{response.json}")



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

    def test_logout_user(self):
        self.login_buyer()
        response = self.session.post(f"{self.url}/api/user/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        self.login_buyer()
        response = self.session.delete(f"{self.url}/api/user/profile")
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()
