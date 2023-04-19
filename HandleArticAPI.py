import requests
import random
import base64
from MakeASCII import prepare


def get_random_page():

    api_url = "https://api.artic.edu/api/v1/artworks"

    params = {
        'limit': 1,
    }

    response = requests.get(api_url, params=params)

    responseJSON = response.json()

    max_page = responseJSON['pagination']['total_pages']

    pageIndex = random.randint(0, max_page-1)

    print("Page random index:", pageIndex)

    return pageIndex


def get_artwork():

    api_url = "https://api.artic.edu/api/v1/artworks"

    pageIndex = get_random_page()

    params = {
        'limit': 1,
        'page': pageIndex,
    }

    # print(params['limit'])

    response = requests.get(api_url, params=params)

    responseJSON = response.json()

    # print(responseJSON)

    artwork_imageid = ""

    artwork_id = ""

    artwork_title = ""

    artist_title = ""

    artwork_display = ""

    artwork_dimensions = ""

    artwork_alttext = ""

    artwork_datestart = ""

    artwork_dateend = ""

    artwork_poo = ""

    artwork_creditline = ""

    artwork_imageid = responseJSON['data'][0]['image_id']

    artwork_id = responseJSON['data'][0]['id']

    artwork_title = responseJSON['data'][0]['title']

    artist_title = responseJSON['data'][0]['artist_title']

    artwork_display = responseJSON['data'][0]['medium_display']

    artwork_dimensions = responseJSON['data'][0]['dimensions']

    # if 'thumbnail' in responseJSON['data'][0]:
    #    if 'alt_text' in responseJSON['data'][0]['thumbnail']:
    #        artwork_alttext = responseJSON['data'][0]['thumbnail']['alt_text']

    artwork_datestart = responseJSON['data'][0]['date_start']

    artwork_dateend = responseJSON['data'][0]['date_end']

    artwork_poo = responseJSON['data'][0]['place_of_origin']

    if 'credit_line' in responseJSON['data'][0]:
        artwork_creditline = responseJSON['data'][0]['credit_line']

    artwork = {

        'artwork_imageid': artwork_imageid,

        'artwork_id': artwork_id,

        'artwork_title': artwork_title,

        'artist_title': artist_title,

        'artwork_display': artwork_display,

        'artwork_dimensions': artwork_dimensions,

        # 'artwork_alttext': artwork_alttext,

        'artwork_datestart': artwork_datestart,

        'artwork_dateend': artwork_dateend,

        'artwork_poo': artwork_poo,

        'artwork_creditline': artwork_creditline,

    }

    return artwork


def prepare_info(artwork):

    artwork_title = artwork['artwork_title']

    artist_title = artwork['artist_title']

    artwork_dimensions = artwork['artwork_dimensions']

    artwork_datestart = artwork['artwork_datestart']

    artwork_dateend = artwork['artwork_dateend']

    #artwork_alttext = artwork['artwork_alttext']

    artwork_poo = artwork['artwork_poo']

    artwork_display = artwork['artwork_display']

    artwork_creditline = artwork['artwork_creditline']

    artwork_date = ""

    if "-" in str(artwork_datestart):
        artwork_datestart = str(artwork_datestart)[1:] + "BC"

    if "-" in str(artwork_dateend):
        artwork_dateend = str(artwork_dateend)[1:] + "BC"

    if (artwork_datestart != '' and artwork_datestart != None) and (artwork_dateend != '' and artwork_dateend != None):
        if artwork_datestart == artwork_dateend:
            artwork_date = artwork_datestart
        else:
            artwork_date = str(artwork_datestart) + "-" + str(artwork_dateend)
    elif (artwork_datestart != '' and artwork_datestart != None):
        artwork_date = artwork_datestart
    else:
        artwork_date = artwork_dateend

    if ";" in artwork_dimensions:
        artwork_dimensions = artwork_dimensions.split(";")[0]

    elimlist = [artwork_title, artist_title,
                artwork_date, artwork_display, artwork_dimensions]

    caption1 = ""

    caption2 = ""

    for element in elimlist:
        if element != None and element != '':
            caption1 = str(caption1) + str(element) + ", "

    caption1 = caption1[:-2]

    print(caption1)

    elimlist = [artwork_creditline, artwork_poo]

    for element in elimlist:
        if element != None and element != '':
            caption2 = str(caption2) + str(element) + ", "

    caption2 = caption2[:-2]

    print(caption2)

    return {
        'caption1': caption1,
        'caption2': caption2
    }


def get_artwork_image(artwork):

    # getting the image with url concatenation

    artwork_imageid = artwork['artwork_imageid']

    urlbase = "https://www.artic.edu/iiif/2/"

    urlend = "/full/843,/0/default.jpg"

    image_url = urlbase + artwork_imageid + urlend

    response = requests.get(image_url)

    # with open('image_name.jpg', 'wb') as handler:
    #    handler.write(response.content)

    if response.status_code == 200:

        image_bytes = response.content

        # making the image a base64 string AUTOMATED

        base64_string = base64.b64encode(image_bytes).decode('utf-8')

        # getting a custom image from base64text file

        #base64_string = base64str

        # print(base64_string)

        return base64_string

    else:

        return None


def prepare_tweet():

    artwork = get_artwork()

    artwork_captions = prepare_info(artwork=artwork)

    artwork_base64 = get_artwork_image(artwork=artwork)

    artwork_ascii_base64 = prepare(artwork_base64, 0.4, False)

    if artwork_ascii_base64 == "fail":
        print("PixelData API Error")
        return None

    with open("/tmp/imagetoshare.png", "wb") as fh:
        fh.write(base64.b64decode(artwork_ascii_base64))

    print("Image Saved")

    result = {
        'caption': artwork_captions['caption1'],
    }

    return result


# prepare_info(get_artwork())
