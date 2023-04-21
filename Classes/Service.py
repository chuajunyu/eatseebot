from .APIClient import APIClient


class Service:
    """
    Provides Services to the telegram bot
    """
    def __init__(self):
        self.api_client = APIClient()

    def is_user_existing(self, telename):
        response = self.api_client.get_user_id(telename)
        if response["code"] == 404:
            return False
        elif response["code"] == 200:
            return True
        
    def create_user(self, telename, age, gender):
        response = self.api_client.create_user(True, telename, age, gender)
        print(response)
        if response["code"] == 200:
            return True
        else:
            return False