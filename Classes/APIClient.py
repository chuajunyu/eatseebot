import requests

from .ConfigManager import ConfigManager

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class APIClient(metaclass = Singleton):
    """
    Handles all API requests that are made to the EatSee Database API

    Will Handle basic errors such as API is down etc, else, will return
    the raw response.
    """
    def __init__(self):
        self.api_ip = ConfigManager().get('API_ip')

    def api_get(self, endpoint, data={}):
        url = self.api_ip + endpoint
        response = requests.get(url, json=data)
        # Include error handling here
        return response

    def api_post(self, endpoint, data={}):
        url = self.api_ip + endpoint
        response = requests.post(url, json=data)
        # Include error handling here
        return response

    def check_server_status(self):
        return self.api_get("/")

    def create_user(self, availability: bool, telename: str, age: int, gender: int):
        data = {
            "availability": availability,
            "telename": telename,
            "age": age,
            "gender": gender
        }
        response = self.api_post("/create_user/", data=data)
        return response.json()
    
    def show_profile(self, telename:str):
        data = {
            "telename": telename
        }
        response = self.api_post("/show_profile/", data=data)
        return response.json()
    
    def get_user_id(self, telename:str):
        data = {
            "telename": telename
        }
        response = self.api_post("/get_user_id/", data=data)
        return response.json()


    def show_age_choices(self):
        response = self.api_post("/show_age_choices")
        return response.json()

    def show_gender_choices(self):
        response = self.api_post("/show_gender_choices")
        return response.json()
    
    def show_cuisine_choices(self):
        response = self.api_post("/show_cuisine_choices")
        return response.json()
    
    def show_diet_choices(self):
        response = self.api_post("/show_diet_choices")
        return response.json()
    

    