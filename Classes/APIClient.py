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
        """Generic HTTP Get Request from the api"""
        url = self.api_ip + endpoint
        try:
            response = requests.get(url, json=data)
        except BaseException as e:
            raise e
        return response

    def api_post(self, endpoint, data={}):
        """Generic HTTP Post Request from the api"""
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
            "user_id": chat_id,
            "telename": telename,
            "age": age,
            "gender": gender
        }
        response = self.api_post("/create_user/", data=data)
        return response.json()
    
    def get_user_id(self, telename:str):
        data = {
            "telename": telename
        }
        response = self.api_post("/get_user_id/", data=data)
        return response.json()
    
    def __get_user_info(self, user_id, url):
        """Generic request to get a certain info using the user_id
        
        Args:
            user_id: chat_id between user and bot
            url: Endpoint url

        Returns:
            response.json(): Response from the api in json format
        """
        data = {
            "user_id": user_id
        }
        response = self.api_post(url, data=data)
        return response.json()

    def check_users_for_user(self, user_id):
        return self.__get_user_info(user_id, "/check_users_for_user/")
    
    def check_queue_for_user(self, user_id):
        return self.__get_user_info(user_id, "/check_queue_for_user/")
    
    def check_chat_for_user(self, user_id):
        return self.__get_user_info(user_id, "/check_chat_for_user/")

    def show_profile(self, user_id):
        return self.__get_user_info(user_id, "/show_profile/")
    
    def select_age_preference(self, user_id):
        return self.__get_user_info(user_id, "/select_age_preferences/")
    
    def select_gender_preference(self, user_id):
        return self.__get_user_info(user_id, "/select_gender_preferences/")
    
    def select_cuisine_preference(self, user_id):
        return self.__get_user_info(user_id, "/select_cuisine_preferences/")
    
    def select_diet_preference(self, user_id):
        return self.__get_user_info(user_id, "/select_diet_preferences/")
    
    def select_pax_preference(self, user_id):
        return self.__get_user_info(user_id, "/select_pax_preferences/")

    def change_age(self, user_id, age):
        data = {
            "user_id": user_id,
            "characteristic": age
        }
        response = self.api_post("/change_age/", data=data)
        return response.json()

    def change_gender(self, user_id, gender):
        data = {
            "user_id": user_id,
            "characteristic": gender
        }
        response = self.api_post("/change_gender/", data=data)
        return response.json()
    
    def __change_preferences(self, user_id, preferences, url):
        """Generic request to change a user's preferences
        
        Args:
            user_id: chat_id between user and bot
            preferences: List of integers corresponding to the index of
                         the choices
            url: API Endpoint URL

        Returns:
            response.json(): API response in json format
        """
        data = {
            "user_id": user_id,
            "preferences": preferences
        }
        response = self.api_post(url, data=data)
        return response.json()

    def change_age_preferences(self, user_id, preferences):
        return self.__change_preferences(user_id, preferences, "/change_age_preferences/")
        
    def change_gender_preferences(self, user_id, preferences):
        return self.__change_preferences(user_id, preferences, "/change_gender_preferences/")

    def change_cuisine_preferences(self, user_id, preferences):
        return self.__change_preferences(user_id, preferences, "/change_cuisine_preferences/")

    def change_diet_preferences(self, user_id, preferences):
        return self.__change_preferences(user_id, preferences, "/change_diet_preferences/")
    
    def change_pax_preferences(self, user_id, preferences):
        return self.__change_preferences(user_id, preferences, "/change_pax_preferences/")

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
        return response.json()
    
    def show_pax_choices(self):
        response = self.api_post("/show_pax_choices/")
        return response.json()
    
    def queue(self, user_id: int):
        data = {
            "user_id": user_id
        }
        response = self.api_post("/queue/", data=data)
        return response.json()
    
    def dequeue(self, user_id:int):
        data = {
            "user_id" : user_id
        }
        response = self.api_post("/dequeue/", data=data)
        return response.json()

    def match(self, user_id:int):
        data = {
            "user_id" : user_id
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

    def delete_chatroom_user(self, user_id_list: list[int]):
        data = {
            "user_id_list" : user_id_list
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
            "user_id" : chatroom_id
        }
        response = self.api_post("/select_chatroom/", data=data)
        return response.json()
