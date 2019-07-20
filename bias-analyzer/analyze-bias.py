import json
import sys
sys.path.insert(0, './..') #Make sure to get the path from the directory above
from main import getRedditListing
import re

#Get rid of the CRAP TOP LEVEL DOMAINS BECAUSE WE DON'T NEED THAT CRAP (mainly so that multinational sites like bbc are handled correctly)
def stripTLDomain(str):
    return re.sub(r"\.((co)|(org)|(net)|(us)|(eu)|(uk)|(ca)).*", "", str)

#Set up the JSON
with open("AllSidesBiasRatings.json", "r") as f:
    #We have use only the JSON (not the comments) or else the JSON parser gives a fit
    bias_data = f.readlines()[6]
    bias_data = json.loads(bias_data)

# print(json.dumps(bias_data, sort_keys = True, indent = 2))

ratings = {
    "left": 0,
    "lean_left": 0,
    "center": 0,
    "lean_right": 0,
    "right": 0,
    "mixed": 0,
    "inconclusive": 0
}
rating_ids = {
    "71": "left",
    "72": "lean_left",
    "73": "center",
    "74": "lean_right",
    "75": "right",
    "2707": "mixed",
    "2690": "inconclusive"
}

#Not so optimized, but whatever
loops = int(sys.argv[5])
i = 0 #Counting
after = None
for loop in range(loops):
    listing = getRedditListing(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], {
        'raw_json' : 1,
        't' : 'week',
        'g' : 'US',
        'limit' : 100,
        'include_categories' : False,
        'after' : after
    })

    after = listing["data"]["after"] #Move on with the listings
    if loop > 0:
        sys.stdout.write("\x1b[1A\x1b[K\r") #Clear the "loop" line on loops greater than the first
    sys.stdout.write("----Loop " + str(loop + 1) + "----\n")


    for thing in listing["data"]["children"]:
        found = False
        i += 1
        sys.stdout.write("["+str(i)+"]: ")
        # print("Stripped top level domain: " + stripTLDomain(thing["data"]["domain"]))
        for site in bias_data:
            #Check if the site matches (stripping the top level domain for reasons stated previously)
            if stripTLDomain(site["url"]) == stripTLDomain(thing["data"]["domain"]):
                sys.stdout.write("Matched " + site["url"])
                ratings[rating_ids[str(site["bias_rating"])]] += 1
                found = True
                break
        if not found:
            sys.stdout.write(thing["data"]["domain"] + " has no match!")
            ratings["inconclusive"] += 1
        sys.stdout.write("\x1b[K\r") #Clear the line
    sys.stdout.flush()

    if after == None:
        print("\nNothing left to analyze! Breaking.")
        break

#Print results
print("The results are in!")
for k,v in ratings.items():
    print(k + ": " + str(round(v/sum(ratings.values())*100, 3)) + "%")
