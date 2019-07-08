# Content Analyzer (for Reddit)
Allows you to (currently only) read Reddit through the console

## Requirements
* Python 3.7
* Python Requests Library

## How to Use
    python main.py [SUBREDDIT] [CLIENT_ID] [CLIENT_SECRET] [sort_method (OPTIONAL)]

* `SUBREDDIT` - Target Subreddit, sans the 'r/' prefix
* `CLIENT_ID` - The ID from a dummy app that you have to create yourself [here.](https://www.reddit.com/prefs/apps) Used for authorization.
* `CLIENT_SECRET` - The secret from a dummy app that you have to create yourself. Used for authorization.
* `sort_method` - An optional string detailing the sort method. Choose from `top`, `best`, `hot`, `rising`, `controversial`, and `new`.
