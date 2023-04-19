from GetMediaID import get_media_id
from HandleTwitterAPI import tweet
from HandleArticAPI import prepare_tweet


def lambda_tweet(event, context):

    captionJSON = prepare_tweet()
    caption = captionJSON['caption']
    mediaid = get_media_id()
    print("Caption: " + str(caption))
    print("Media ID: " + str(mediaid))
    imageObject = {"media_ids": [str(mediaid)]}
    tweet(caption=caption, image=imageObject)

    return "tweeted"
