from .APIClient import APIClient
from .KeyboardGenerator import KeyboardGenerator


class Service:
    """
    Provides Services to the telegram bot by calling on the APIClient
    to make the appropriate API requests, and handling any additional
    logic.

    Handles any errors or bad response codes returned by the API.
    """
    def __init__(self):
        self.api_client = APIClient()
        self.keyboard_generator = KeyboardGenerator()
        self.cache = dict()

    def is_user_existing(self, telename):
        response = self.api_client.get_user_id(telename)
        
        
        if response["code"] == 404:
            return False
        elif response["code"] == 200:
            return True
    def get_user_id(self, telename):
        response = self.api_client.get_user_id(telename)
        
        
        if response["code"] == 404:
            return False
        elif response["code"] == 200:
            data = response["data"]
            return data
        
    def create_user(self, chat_id, telename, age, gender):
        response = self.api_client.create_user(chat_id, telename, age, gender)
        if response["code"] == 200:
            return True
        else:
            return False
        
    def show_profile(self, telename):
        response = self.api_client.show_profile(telename)
        if response["code"] == 200:
            data = response["data"]
            return data
        else:
            return False
           
    def select_user_age_pref(self, telename):
        response = self.api_client.select_age_preference(telename)
        if response["code"] == 200:
            return [str(i) for i in response["data"]]
        else:
            return False
        
    def select_user_gender_pref(self, telename):
        response = self.api_client.select_gender_preference(telename)
        if response["code"] == 200:
            return [str(i) for i in response["data"]]
        else:
            return False
    
    def select_user_cuisine_pref(self, telename):
        response = self.api_client.select_cuisine_preference(telename)
        if response["code"] == 200:
            return [str(i) for i in response["data"]]
        else:
            return False
        
    def select_user_diet_pref(self, telename):
        response = self.api_client.select_diet_preference(telename)
        if response["code"] == 200:
            return [str(i) for i in response["data"]]
        else:
            return False
        
    def get_age_choices(self):
        if "get_age_choices" in self.cache:
            return self.cache["get_age_choices"]
        else:
            response = self.api_client.show_age_choices()
            if response["code"] == 200:
                return response["data"]["age"]
            
    def get_gender_choices(self):
        if "get_gender_choices" in self.cache:
            return self.cache["get_gender_choices"]
        else:
            response = self.api_client.show_gender_choices()
            if response["code"] == 200:
                return response["data"]["gender"]
            
    def get_cuisine_choices(self):
        if "get_cuisine_choices" in self.cache:
            return self.cache["get_cuisine_choices"]
        else:
            response = self.api_client.show_cuisine_choices()
            if response["code"] == 200:
                return response["data"]["cuisine"]
            
    def get_diet_choices(self):
        if "get_diet_choices" in self.cache:
            return self.cache["get_diet_choices"]
        else:
            response = self.api_client.show_diet_choices()
            if response["code"] == 200:
                return response["data"]["diet"]
            
    def change_age(self, telename, age):
        response = self.api_client.change_age(telename, age)
        if response["code"] == 200:
            return True
        else:
            return False
        
    def change_gender(self, telename, gender):
        response = self.api_client.change_gender(telename, gender)
        if response["code"] == 200:
            return True
        else:
            return False
        
    def change_age_preferences(self, telename, preferences):
        response = self.api_client.change_age_preferences(telename, preferences)
        if response["code"] == 200:
            return True
        else:
            return False
    
    def change_gender_preferences(self, telename, preferences):
        response = self.api_client.change_gender_preferences(telename, preferences)
        if response["code"] == 200:
            return True
        else:
            return False
    
    def change_cuisine_preferences(self, telename, preferences):
        response = self.api_client.change_cuisine_preferences(telename, preferences)
        if response["code"] == 200:
            return True
        else:
            return False
    
    def change_diet_preferences(self, telename, preferences):
        response = self.api_client.change_diet_preferences(telename, preferences)
        if response["code"] == 200:
            return True
        else:
            return False
    
        
    def queue_user(self, telename):
        response = self.api_client.queue(telename)
        
        if response["code"] == 200:
            return True
        else:
            return False
    
    def dequeue_user(self, telename):
        response = self.api_client.dequeue(telename)
        if response["code"] == 200:
            return True
        else:
            return False
        
    def match_user(self, telename):
        response = self.api_client.match(telename)
        if response["code"] == 200:
            data = response["data"]
            return data
        else:
            return False
    
    def add_chatroom_user(self, chatroom_id, user_id):
        response = self.api_client.add_chatroom_user(chatroom_id, user_id)
        if response["code"] == 200:
            return True
        else:
            return False
        
    def delete_chatroom_user(self, user_id):
        response = self.api_client.delete_chatroom_user_chatroom_user(user_id)
        if response["code"] == 200:
            return True
        else:
            return False
        
    def select_chatroom_user(self, chatroom_id):
        response = self.api_client.select_chatroom_user(chatroom_id)
        if response["code"] == 200:
            data = response["data"]
            return data
        else:
            return False
    
    def select_chatroom(self, chatroom_id):
        response = self.api_client.select_chatroom(chatroom_id)
        if response["code"] == 200:
            data = response["data"]
            return data
        else:
            return False

