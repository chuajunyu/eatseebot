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
        try:
            response = requests.get(url, json=data)
        except BaseException as e:
            raise e
        return response

    def api_post(self, endpoint, data={}):
        url = self.api_ip + endpoint
        try:
            response = requests.post(url, json=data)
        except BaseException as e:
            raise e
        return response

    def check_server_status(self):
        return self.api_get("/")

    def create_user(self, chat_id, telename: str, age: int, gender: int):
        data = {
            "id": chat_id,
            "telename": telename,
            "age": age,
            "gender": gender
        }
        response = self.api_post("/create_user/", data=data)
        return response.json()
    
    def __get_user_info(self, telename, url):
        data = {
            "telename": telename
        }
        response = self.api_post(url, data=data)
        return response.json()

    def show_profile(self, telename:str):
        return self.__get_user_info(telename, "/show_profile/")
    
    def get_user_id(self, telename:str):
        return self.__get_user_info(telename, "/get_user_id/")
    
    def select_age_preference(self, telename):
        return self.__get_user_info(telename, "/select_age_preferences/")
    
    def select_gender_preference(self, telename):
        return self.__get_user_info(telename, "/select_gender_preferences/")
    
    def select_cuisine_preference(self, telename):
        return self.__get_user_info(telename, "/select_cuisine_preferences/")
    
    def select_diet_preference(self, telename):
        return self.__get_user_info(telename, "/select_diet_preferences/")

    def change_age(self, telename, age):
        data = {
            "telename": telename,
            "characteristic": age
        }
        response = self.api_post("/change_age/", data=data)
        print(response)
        return response.json()

    def change_gender(self, telename, gender):
        data = {
            "telename": telename,
            "characteristic": gender
        }
        response = self.api_post("/change_gender/", data=data)
        return response.json()
    
    def __change_preferences(self, telename, preferences, url):
        data = {
            "telename": telename,
            "preferences": preferences
        }
        response = self.api_post(url, data=data)
        return response.json()

    def change_age_preferences(self, telename, preferences):
        return self.__change_preferences(telename, preferences, "/change_age_preferences/")
        
    def change_gender_preferences(self, telename, preferences):
        return self.__change_preferences(telename, preferences, "/change_gender_preferences/")

    def change_cuisine_preferences(self, telename, preferences):
        return self.__change_preferences(telename, preferences, "/change_cuisine_preferences/")

    def change_diet_preferences(self, telename, preferences):
        return self.__change_preferences(telename, preferences, "/change_diet_preferences/")

    def show_age_choices(self):
        response = self.api_post("/show_age_choices/")
        return response.json()

    def show_gender_choices(self):
        response = self.api_post("/show_gender_choices/")
        return response.json()
    
    def show_cuisine_choices(self):
        response = self.api_post("/show_cuisine_choices/")
        return response.json()
    
    def show_diet_choices(self):
        response = self.api_post("/show_diet_choices/")
        print(response.json())
        return response.json()
    
    def queue(self, telename:str):
        data = {
            "telename": telename
        }
        response = self.api_post("/queue/", data=data)
        
        
        return response.json()
    
    def dequeue(self, telename:str):
        data = {
            "telename": telename
        }
        response = self.api_post("/dequeue/", data=data)
        return response.json()

    def match(self, telename:str):
        data = {
            "telename": telename
        }
        response = self.api_post("/match/", data=data)
        return response.json()

    def add_chatroom_user(self, chatroom_id: int, user_id: list[int]):
        data = {
            "chatroom_id" : chatroom_id,
            "user_id" : user_id
        }
        response = self.api_post("/add_chatroom_user/", data=data)
        return response.json()

    def delete_chatroom_user(self, user_id: list[int]):
        data = {
            "user_id" : user_id
        }
        response = self.api_post("/delete_chatroom_user/", data=data)
        return response.json()

    def select_chatroom_user(self, chatroom_id : int):
        data = {
            "chatroom_id" : chatroom_id
        }
        response = self.api_post("/select_chatroom_user/", data=data)
        return response.json()
    
    def select_chatroom(self, chatroom_id: int):
        data = {
            "chatroom_id" : chatroom_id
        }
        response = self.api_post("/select_chatroom/", data=data)
        return response.json()
