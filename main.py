#TODO: Go through STDOUT to maybe get better browsing

import requests as req
import sys
import base64
import json
from PIL import Image
from io import BytesIO
from imagetoansi import image_to_ansi
import textwrap as tw

def getRedditListing(subreddit, client_id, client_secret, sort_method = "top", info_payload = {
    'raw_json' : 1,
    't' : 'day', #Time amount for top and controversial
    'g' : 'US', #Region for hot
    'limit' : 100,
    'include_categories' : False
}):
    #Required for HTTP Basic Authorization
    auth = client_id+":"+client_secret
    auth_encoded = base64.b64encode(auth.encode('utf-8')) #Needs to be a string in the header later

    #Check if the sort_method was chosen from one of the available sort methods
    while sort_method not in ["top", "best", "hot", "rising", "controversial", "new"]:
        print("Not a correct sort method. Please choose from 'top', 'best', 'hot', 'rising', 'new', and 'controversial'.")
        exit()

    #The nitty gritty
    with req.session() as s:
        #The initial payload to post so we can get the access token
        s.headers.update({
            'Authorization' : 'Basic ' + str(auth_encoded, "utf-8"),
            'User-Agent' : 'reddit-content-analyzer/0.0.1'
        })
        initial_payload = {
            'grant_type' : 'client_credentials'
        }
        response = s.post("https://www.reddit.com/api/v1/access_token", data=initial_payload)
        # print(response.json())
        #Now to get the info
        response = s.get('http://www.reddit.com/r/' + subreddit + '/' + sort_method + "/.json", params=info_payload)
        content_list = response.json()
        # print(json.dumps(content_list, indent=2, sort_keys=True)) #Prettyprint the JSON, but just for debugging
        return content_list

#The thing we're probably looking for is its `domain` for websites
def printRedditListing(listing):
    for i in listing["data"]["children"]:
        print(u"[\u001b[4mr/" + i["data"]["subreddit"] + u"\u001b[0m] From \u001b[7mu/" + i["data"]["author"] + u"\u001b[0m: '" + i["data"]["title"] + "' with " + str(i["data"]["ups"]-i["data"]["downs"]) + " points")
        try: #Get preview images
            img = req.get(i["data"]["preview"]["images"][0]["resolutions"][0]["url"])
            img = Image.open(BytesIO(img.content)) #Read the data
            img = img.resize((32, 32)) #Resize it to give it that great console feel
            image_to_ansi(img)
        except: #Print text, wrapped correctly
            split_text = (i["data"]["selftext"]).splitlines()
            wrapped_text = []
            for i in range(len(split_text)): #Split the text by newlines so we can keep the newlines in the text itself
                wrapped_text.append(tw.wrap(split_text[i], width = 64))
            for i in range(len(wrapped_text)):
                if type(wrapped_text[i]) == str:
                    print(tw.indent(wrapped_text[i], "\t")) #Indent, which makes it look nice
                elif len(wrapped_text[i]) > 0: #Made to fix a bug where way too many newlines were made
                    for j in range(len(wrapped_text[i])):
                        print(tw.indent(wrapped_text[i][j], "\t"))
                    print("\n") #Print another newline to make it look nice

#Main
def main():
    if len(sys.argv) >= 3:
        try: listing = getRedditListing(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
        except: listing = getRedditListing(sys.argv[1],sys.argv[2],sys.argv[3])
        printRedditListing(listing)
    else:
        print("Please input a subreddit, sans the 'r/'. You may also be missing your client id and secret, which you can get at 'https://www.reddit.com/prefs/apps'.")
        print("python main.py [SUBREDDIT] [CLIENT_ID] [CLIENT_SECRET] [sort_method (OPTIONAL)]")

if __name__ == "__main__":
    main()
