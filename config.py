from dotenv import load_dotenv
import os
import json


class Config:

    def __init__(self):
        load_dotenv()

        self.params = {
            'access_token': os.environ.get("IG_ACCESS_TOKEN"),
            'client_id': os.environ.get("IG_APP_ID"),
            'client_secret': os.environ.get("IG_APP_SECRET"),
            'fb_page_id': "1137350566412530",
            'fb_user_id': "1193679667748350",
            'ig_user_id': "17841400911152018",
            'fb_base': "https://graph.facebook.com/",
            'ig_base': "https://graph.instagram.com/",
            'graph_version': 'v11.0',
        }

        self.params['fb_graph_api'] = self.params['fb_base'] + self.params['graph_version'] + '/'
        self.params['ig_graph_api'] = self.params['ig_base'] + self.params['graph_version'] + '/'
        self.params['debug'] = False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.params})"


    def __str__(self):
        return f"{self.__class__.__name__}({json.dumps(self.params, indent=2)})"

    def get_params(self):
        return self.params

