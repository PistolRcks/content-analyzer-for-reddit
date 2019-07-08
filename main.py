import requests as req
import sys
import base64
import json
from PIL import Image
from io import BytesIO
from imagetoansi import image_to_ansi
import textwrap as tw

if len(sys.argv) >= 4:
    SUBREDDIT = sys.argv[1]
    CLIENT_ID = sys.argv[2]
    CLIENT_SECRET = sys.argv[3]

    #Required for HTTP Basic Authorization
    AUTH = CLIENT_ID+":"+CLIENT_SECRET
    AUTH_ENCODED = base64.b64encode(AUTH.encode('utf-8')) #Needs to be a string in the header later

    try: SORT_METHOD = str(sys.argv[4])
    except: SORT_METHOD = "top"
    #Check if the SORT_METHOD was chosen from one of the available sort methods
    while SORT_METHOD not in ["top", "best", "hot", "rising", "controversial", "new"]:
        print("Not a correct sort method. Please choose from 'top', 'best', 'hot', 'rising', 'new', and 'controversial'.")
        exit()

    #The nitty gritty
    with req.session() as s:
        #The initial payload to post so we can get the access token
        s.headers.update({
            'Authorization' : 'Basic ' + str(AUTH_ENCODED, "utf-8"),
            'User-Agent' : 'reddit-content-analyzer/0.0.1'
        })
        initial_payload = {
            'grant_type' : 'client_credentials'
        }
        response = s.post("https://www.reddit.com/api/v1/access_token", data=initial_payload)
        # print(response.json())
        #Now to get the info
        info_payload = {
            'raw_json' : 1,
            't' : 'day', #Time amount for top and controversial
            'g' : 'US', #Region for hot
            'count' : 1,
            'limit' : 100,
            'include_categories' : False
        }
        response = s.get('http://www.reddit.com/r/' + SUBREDDIT + '/' + SORT_METHOD + "/.json", params=info_payload)
        content_list = response.json()
        # print(json.dumps(content_list, indent=2, sort_keys=True)) #Prettyprint the JSON, but just for debugging
        #The thing we're probably looking for is its `domain` for websites
        for i in content_list["data"]["children"]:
            print(u"[\u001b[4mr/" + i["data"]["subreddit"] + u"\u001b[0m] From \u001b[7mu/" + i["data"]["author"] + u"\u001b[0m: '" + i["data"]["title"] + "' with " + str(i["data"]["ups"]-i["data"]["downs"]) + " points")
            try: #Get preview images
                imgdata = s.get(i["data"]["preview"]["images"][0]["resolutions"][0]["url"])
                img = Image.open(BytesIO(imgdata.content))
                img = img.resize((32, 32)) #Resize it to give it that great console feel
                image_to_ansi(img)
            except: print(tw.indent((i["data"]["selftext"]) + "\n", "\t"))
else:
    print("Please input a subreddit, sans the 'r/'. You may also be missing your client id and secret, which you can get at 'https://www.reddit.com/prefs/apps'.")
    print("python main.py [SUBREDDIT] [CLIENT_ID] [CLIENT_SECRET] [sort_method (OPTIONAL)]")
