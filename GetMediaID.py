import tweepy


from TwitterTokens import api_key, api_key_secret, bearer_token, access_token, access_token_secret, client_id, client_secret


def get_media_id():

    auth = tweepy.OAuthHandler(api_key, api_key_secret)

    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    media = api.media_upload("/tmp/imagetoshare.png")

    mediastr = media.media_id

    return mediastr
