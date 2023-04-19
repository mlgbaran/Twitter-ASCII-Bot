import json
from requests_oauthlib import OAuth1Session
from GetMediaID import get_media_id

from TwitterTokens import api_key, api_key_secret, bearer_token, access_token, access_token_secret, client_id, client_secret


def tweet(caption, image):

    payload = {"text": caption,
               "media": image}

    
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(api_key, client_secret=api_key_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the api_key or api_key_secret you entered."
        )

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    
    # Make the request
    oauth = OAuth1Session(
        api_key,
        client_secret=api_key_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

