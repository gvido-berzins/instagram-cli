"""
*** constants.py ***
"""

import os
import requests

ROOT = os.path.dirname(__file__)

PUBLISH_DIR = os.path.join(ROOT, 'to_post')
FEED_DIR = os.path.join(PUBLISH_DIR, 'feed')
STORY_DIR = os.path.join(PUBLISH_DIR, 'stories')

# URL
FILE_SERVER_API = "http://127.0.0.1:4040/api/tunnels"
FILE_SERVER = requests.get(FILE_SERVER_API).json()['tunnels'][0]['public_url'] + '/'

REDIRECT_URL = FILE_SERVER + 'login?state="{st=state123abc,ds=123456789}"'

# Endpoints for Instagram
IG_USER_MEDIA = '{ig-user-id}/media'
IG_USER_MEDIA_PUBLISH = '{ig-user-id}/media_publish'

LONG_LIVED_TOKEN_ENDPOINT = "oauth/access_token"
REFRESH_TOKEN_ENDPOINT = "refresh_access_token"
DEBUG_TOKEN_ENDPOINT = "debug_token"
OAUTH_ENDPOINT = "dialog/oauth"

# Scopes
SCOPES = "user_birthday,user_hometown,user_location,user_likes,user_events,user_photos,user_videos,user_friends,user_posts,user_gender,user_link,user_age_range,email,read_insights,publish_video,catalog_management,gaming_user_locale,user_managed_groups,groups_show_list,pages_manage_cta,pages_manage_instant_articles,pages_show_list,read_page_mailboxes,ads_management,ads_read,business_management,pages_messaging,pages_messaging_phone_number,pages_messaging_subscriptions,instagram_basic,instagram_manage_comments,instagram_manage_insights,instagram_content_publish,publish_to_groups,groups_access_member_info,leads_retrieval,whatsapp_business_management,instagram_manage_messages,attribution_read,page_events,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_ads,pages_manage_posts,pages_manage_engagement,public_profile,basic_info"


# Paths

"""

Request URL:
https://developers.facebook.com/tools/app/985798668897126/async/perms/?version=v11.0&access_token=EAAOAlCN6y2YBALSvgwv9EOZASZAuFIrzbLRdvHWHcSmxbykKwnJqLEPhp9EwKpdzEACOjZAd0iwRV5WmjvVZCIBUBCLmGcZAnLXQLdnzCGZCplHSSlXqFQEAWh5QfrHPudvd3YZAIMTZCiqwN7c1mdTfbhTM3ehujGy038EYJfxY4zzfDSz444KLPmdjB3M9zLKkWYWZCdiM0gh4NZB44xoyX1bSk082wjluwWfTE26pkUuB8ujFhuuXZCd
"""

