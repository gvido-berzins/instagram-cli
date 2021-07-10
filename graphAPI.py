from constants import (
    IG_USER_MEDIA, IG_USER_MEDIA_PUBLISH,
    REDIRECT_URL, OAUTH_ENDPOINT,
    LONG_LIVED_TOKEN_ENDPOINT, DEBUG_TOKEN_ENDPOINT,
    REFRESH_TOKEN_ENDPOINT, SCOPES,
    STORY_DIR, FILE_SERVER,
)

from urllib import parse

import requests
import json
import time
import pyperclip


class GraphAPI:

    def __init__(self, config):
        self.config = config

    def get_config(self):
        return self.config

    def make_api_call(self, url, method='GET', params={}, access_token_required=False, debug=False):

        debug = self.config['debug']

        if method == 'GET':
            call = requests.get
        elif method == 'POST':
            call = requests.post
        else:
            print(f"Unknown method - {method}")
            exit(1)

        if access_token_required:
            params['access_token'] = self.config['access_token']

        api_response = call(url, params=params)
        print(api_response.text)

        response = {}
        response['url'] = url
        response['params'] = params
        response['api_response'] = api_response.json()

        if debug:
            self.display_api_response(response)

        return response

    @staticmethod
    def display_api_response(response):

        print("=============== URL       ===============")
        print(response['url'])

        print("=============== PARAMS    ===============")
        print(json.dumps(response['params'], indent=2))

        print("=============== RESPONSE  ===============")
        print(json.dumps(response['api_response'], indent=2))

    @staticmethod
    def url_encode_dict(dict_):
        if bool(dict_):
            new_dict_ = dict_
            for k, v in dict_.items():
                new_dict_[k] = parse.quote(v)

            return new_dict_
        return dict_

    def get_access_token(self, params={}):
        """
        https://www.facebook.com/v11.0/dialog/oauth?
          client_id={app-id}
          &redirect_uri={redirect-uri}
          &state={state-param}
          &scopes=scopes
        """
        params = {
            'client_id': self.config['client_id'], # 985798668897126
            'client_secret': self.config['client_secret'], # 985798668897126
            'redirect-uri': REDIRECT_URL,
            'state': "{st=state123abc,ds=123456789}",
            'scopes': SCOPES,
        }

        url = self.url.replace('graph', 'www') + OAUTH_ENDPOINT + '?'
        params = self.url_encode_dict(params)

        for p in params:
            url += params[p]

        print(url)
        exit()
        # return self.make_api_call(url, params=params)

    def get_user_long_lived_token(self, params={}):
        """
        curl -i -X GET "https://graph.facebook.com/{graph-api-version}/oauth/access_token?
            grant_type=fb_exchange_token&
            client_id={app-id}&
            client_secret={app-secret}&
            fb_exchange_token={your-access-token}"
        """
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': self.config['client_id'],
            'client_secret': self.config['client_secret'],
            'fb_exchange_token': self.config['access_token']
        }
        url = self.url + LONG_LIVED_TOKEN_ENDPOINT
        return self.make_api_call(url, params=params)

    def get_user_refresh_token(self, params={}): # May be wrong
        """
        GET https://graph.instagram.com/refresh_access_token
          ?grant_type=ig_refresh_token
          &access_token={long-lived-access-token}

        Token JSON:
        {
          "data": {
            "app_id": "985798668897126",
            "type": "USER",
            "application": "CLI helper",
            "data_access_expires_at": 1633520017,
            "expires_at": 1630920444,
            "is_valid": true,
            "issued_at": 1625736444,
            "scopes": [ ...  ],
            "granular_scopes": [ { "scope": "..." }, ...  ],
            "user_id": "1193679667748350"
          }
        }
        """
        params = {
            'grant_type': 'ig_refresh_token',
        }
        url = self.url + REFRESH_TOKEN_ENDPOINT
        return self.make_api_call(url, params=params, access_token_required=True)

    def get_debug_token(self, params={}):

        """
        curl -i -X GET "https://graph.facebook.com/debug_token?
          input_token={input-token}&
          access_token={valid-access-token}
        """
        params = {
            'input_token': self.config['access_token'],
        }
        url = self.url + DEBUG_TOKEN_ENDPOINT
        return self.make_api_call(url, params=params, access_token_required=True)


class InstagramAPI(GraphAPI):

    def __init__(self, config):
        super().__init__(config)
        self.user_id = config['ig_user_id']
        self.url = config['fb_graph_api']

    def get_ig_user_id(self):
        """
        GET /{page-id}/?fields=instagram_business_account
        """
        params = {
            'fields': 'instagram_business_account'
        }

        url = self.url + self.config['fb_page_id']
        return super().make_api_call(url, params=params, access_token_required=True)

    def get_user_media(self, params={}):
        """
        GET /{ig-user-id}/media
        """
        endpoint = IG_USER_MEDIA.replace('{ig-user-id}', self.user_id)
        url = self.url + endpoint
        return super().make_api_call(url, access_token_required=True)

    def publish_story(self, filename, params={}):
        pass

    def publish_image(self, metadata, params={}):
        creation_id = self.create_container(metadata, 'IMAGE')
        return self.media_publish(creation_id)

    def publish_video(self, metadata, params={}):
        creation_id = self.create_container(metadata, 'VIDEO')
        return self.media_publish(creation_id)

    def media_publish(self, creation_id):
        """
        POST /{ig-user-id}/media_publish?creation_id={creation_id}
        """
        params = {
            'creation_id': creation_id,
        }

        self.check_media_status(creation_id)  # Container needs to be first uploaded before publishing

        endpoint = IG_USER_MEDIA_PUBLISH.replace('{ig-user-id}', self.user_id)
        url = self.url + endpoint

        return super().make_api_call(url, method='POST', params=params, access_token_required=True)

    def create_container(self, metadata, media_type):
        """
        POST graph.facebook.com/17841400008460056/media
          ?media_type=VIDEO
          &video_url=https//www.example.com/videos/hungry-fonzes.mov
          &caption=%23Heyyyyyyyy!
        """
        url_key = 'image_url' if media_type == "IMAGE" else "video_url"

        params = {
            'media_type': media_type,
            url_key: FILE_SERVER + metadata['filename'],
            'caption': metadata['caption'],
        }

        endpoint = IG_USER_MEDIA.replace('{ig-user-id}', self.user_id)
        url = self.url + endpoint
        response = super().make_api_call(url, method='POST', params=params, access_token_required=True)

        return int(response['api_response']['id'])

    def check_media_status(self, creation_id):
        """
        GET /{ig-container-id}

        fields = id, status_code

        status_code:
            EXPIRED — The container was not published within 24 hours and has expired.
            ERROR — The container failed to complete the publishing process.
            FINISHED — The container and its media object are ready to be published.
            IN_PROGRESS — The container is still in the publishing process.
            PUBLISHED — The container's media object has been published.
        """
        finished = False
        params = {
            'fields': 'id,status_code'
        }
        endpoint = str(creation_id)
        url = self.url + endpoint

        while not finished:
            response = super().make_api_call(url, method='GET', params=params, access_token_required=True)
            status_code = response['api_response']['status_code']

            if status_code != 'IN_PROGRESS':
                print(f"*** {status_code} ***")
                finished = True
            else:
                print("> Waiting 2 seconds.")
                time.sleep(2)


