import json
import os
import sys
from datetime import datetime, timezone
import curl_cffi
from oauthlib.oauth1 import Client
from typing import Any

CONSUMER_KEY = '3nVuSoBZnx6U4vzUxf5w'
CONSUMER_SECRET = 'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'


def getOauth(url:str, http_method: Any, body: Any, headers: Any,  oauth_token: str, oauth_token_secret: str):
    client = Client(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
        signature_method="HMAC-SHA1",
        realm="http://api.twitter.com/"
    )

    _uri, headers, _body = client.sign(
        uri=url,
        http_method=http_method,
        body=body,
        headers=headers
    )
    return headers["Authorization"]

def graphqlUserWithProfileTweetsQueryV2(oauth_token: str, oauth_token_secret: str):
    url = "https://api.twitter.com/graphql/9ztWBTUMXnojmwaMLHPiDQ/UserWithProfileTweetsQueryV2"
    json_payload = {
        "features": "{\"grok_translations_community_note_translation_is_enabled\":false,\"super_follow_badge_privacy_enabled\":true,\"longform_notetweets_rich_text_read_enabled\":true,\"super_follow_user_api_enabled\":true,\"profile_label_improvements_pcf_label_in_profile_enabled\":true,\"premium_content_api_read_enabled\":false,\"grok_translations_community_note_auto_translation_is_enabled\":false,\"android_graphql_skip_api_media_color_palette\":true,\"tweetypie_unmention_optimization_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"subscriptions_verification_info_enabled\":true,\"blue_business_profile_image_shape_enabled\":true,\"super_follow_exclusive_tweet_notifications_enabled\":true,\"longform_notetweets_inline_media_enabled\":true,\"grok_android_analyze_trend_fetch_enabled\":false,\"unified_cards_ad_metadata_container_dynamic_card_content_query_enabled\":true,\"super_follow_tweet_api_enabled\":true,\"articles_api_enabled\":true,\"creator_subscriptions_tweet_preview_api_enabled\":true,\"freedom_of_speech_not_reach_fetch_enabled\":true,\"grok_translations_timeline_user_bio_auto_translation_is_enabled\":false,\"grok_translations_post_auto_translation_is_enabled\":false,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":true,\"immersive_video_status_linkable_timestamps\":true,\"profile_label_improvements_pcf_label_in_post_enabled\":true}",
        "variables": "{\"includeTweetImpression\":true,\"includeHasBirdwatchNotes\":false,\"includeEditPerspective\":false,\"includeEditControl\":true,\"count\":20,\"rest_id\":\"91478624\",\"includeTweetVisibilityNudge\":true,\"autoplay_enabled\":true}"
    }
    oauth = getOauth(url=url, http_method="POST", body=None, headers={"Content-Type": "application/json"}, oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
    req_headers = {
        "accept": "application/json",
        "x-twitter-client": "TwitterAndroid",
        "user-agent": "TwitterAndroid/11.24.0-release.0 (311240000-r-0) SM-G9900/12 (Samsung;SM-G9900;Samsung;r9q;0;;1;2015)",
        "accept-encoding": "br, gzip, deflate",
        "x-twitter-client-language": "en-US",
        "authorization": oauth,
        "x-twitter-client-version": "11.24.0-release.0",
        "cache-control": "no-store",
        "x-twitter-active-user": "yes",
        "x-twitter-api-version": "5",
        "accept-language": "en-US",
        "x-twitter-client-flavor": "",
        "content-type": "application/json",
    }
    r = curl_cffi.post(url, impersonate="chrome_android", json=json_payload, headers=req_headers, default_headers=False)
    r.raise_for_status()
    return r.json()

def main(oauth_token: str, oauth_token_secret: str):
    # Fetch data
    data = graphqlUserWithProfileTweetsQueryV2(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)

    # Save to file
    os.makedirs("./tweets", exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    file_path = f"./tweets/{timestamp}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ tweets saved to {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py [oauth_token] [oauth_token_secret]")
        sys.exit(1)

    oauth_token = sys.argv[1]
    oauth_token_secret = sys.argv[2]

    main(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
