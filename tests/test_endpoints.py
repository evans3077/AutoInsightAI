import requests

BASE_URL = "http://127.0.0.1:8000/api"

def test_text_endpoint():
    response = requests.get(f"{BASE_URL}/process-text/", params={"text": "Hello World"})
    print("Text Endpoint Response:", response.json())

def test_image_endpoint():
    response = requests.get(f"{BASE_URL}/process-image/", params={"image_path": "./tests/sample.jpg"})
    print("Image Endpoint Response:", response.json())

def test_user_registration():
    data = {"username": "tester", "password": "test123"}
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print("Register Response:", response.json())

def test_user_login():
    data = {"username": "tester", "password": "test123"}
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print("Login Response:", response.json())

if __name__ == "__main__":
    test_text_endpoint()
    test_image_endpoint()
    test_user_registration()
    test_user_login()
