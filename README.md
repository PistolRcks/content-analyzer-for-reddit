# Content Analyzer (for Reddit)
Allows you to (currently only) read Reddit through the console and get Listings from Reddit

## Requirements
* [Python 3.7](https://www.python.org/downloads/)
* [Requests](https://pypi.org/project/requests/)
* [Pillow](https://pypi.org/project/Pillow/)

## Usage
    python main.py [SUBREDDIT] [CLIENT_ID] [CLIENT_SECRET] [sort_method (OPTIONAL)]

* `SUBREDDIT` - Target Subreddit, sans the 'r/' prefix
* `CLIENT_ID` - The ID from a dummy app that you have to create yourself [here.](https://www.reddit.com/prefs/apps) Used for authorization.
* `CLIENT_SECRET` - The secret from a dummy app that you have to create yourself. Used for authorization.
* `sort_method` - An optional string detailing the sort method. Choose from `top`, `best`, `hot`, `rising`, `controversial`, and `new`.

## Credits
* [image-to-ansi.py](https://gist.github.com/klange/1687427) by Kevin Lange and Micah Eliott
* Bias Ratings (`bias-analyzer/AllSidesBiasRatings.json`) from [AllSides.com](https://www.allsides.com/unbiased-balanced-news)

## LICENSE NOTICE
All code in this repository is licensed under GPLv3 ***EXCEPT FOR*** the AllSides.com Bias Ratings file (`bias-analyzer/AllSidesBiasRatings.json`), which is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License.](https://creativecommons.org/licenses/by-nc/4.0/) A copy of the license notice is also included in the file.
