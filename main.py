from graphAPI import (
    InstagramAPI,
)

from config import Config


def main():
    c = Config()
    conf = c.get_params()
    conf['debug'] = True

    ig_api = InstagramAPI(conf)

    # ig_api.get_ig_user_id()
    # ig_api.get_user_long_lived_token()
    # ig_api.get_access_token()
    # ig_api.get_debug_token()
    user_media = ig_api.get_user_media()

    video_metadata = {
        'filename': 'story1.mov',
        'caption': 'Testing the api, will delete this soon. \n\n#api'
    }
    image_metadata = {
        'filename': 'image.jpg',
        'caption': 'Testing the api, will delete this soon. \n\n#api'
    }


    # ig_api.publish_video(video_metadata)
    # ig_api.publish_image(image_metadata)




if __name__ == '__main__':
    main()


## Process on getting it done
# 1. Create the app
# 2. Get access token from Graph API Explorer
# - https://developers.facebook.com/tools/explorer/
# 3. Switch to a proffessional account
# 4. Create facebook page
# 5. Get the facebook page ID
# - Facebook Page >> About >> More Info >> Page ID
# 6. Connect the IG user to the page
# - Settings >> Instagram >> Connect
# 7. GET /{page-id}/?fields=instagram_business_account
# - Now we have our Instagram account ID
# 8. Have fun!
# Last step is to make a function to refresh the access token.

