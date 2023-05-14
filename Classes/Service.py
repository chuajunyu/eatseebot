from .APIClient import APIClient


class Service:
    """
    Provides Services to the telegram bot by calling on the APIClient
    to make the appropriate API requests, and handling any additional
    logic.

    Handles any errors or bad response codes returned by the API.
    """
    def __init__(self):
        self.api_client = APIClient()

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
        
    def create_user(self, telename, age, gender):
        response = self.api_client.create_user(True, telename, age, gender)
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

