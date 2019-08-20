# bias-analyzer (utilizing reddit-content-analyzer)
## Why?
I had started to notice that most link posts in reddit's [r/news](https://www.reddit.com/r/news) and [r/worldnews](https://www.reddit.com/r/worldnews) were fairly leftist in nature. So, that was my hypothesis, and this was made to test it!

## Requirements
* Everything from the main README
* [Matplotlib](https://matplotlib.org/)

## How to Use
    python analyze-bias.py [SUBREDDIT] [CLIENT_ID] [CLIENT_SECRET] [SORT_METHOD] [TIMEFRAME] [LISTINGS]

(NB: Most arguments are exactly the same as the in main.py!)
* `SUBREDDIT` - Target subreddit, sans the 'r/' prefix
* `CLIENT_ID` - The ID from a dummy app that you have to create yourself [here.](https://www.reddit.com/prefs/apps) Used for authorization.
* `CLIENT_SECRET` - The secret from a dummy app that you have to create yourself. Used for authorization.
* `SORT_METHOD` - A string detailing the sort method. Choose from `top`, `best`, `hot`, `rising`, `controversial`, and `new`.
* `TIMEFRAME` - A string detailing the timeframe from which to get the posts. Choose from the last `hour`, `day`, `week`, `month`, `year`, or from `all` posts.
* `LISTINGS` - The integer amount of listings of 100 different reddit posts to analyze (i.e. One listing will contain 100 reddit posts, and two will contain 200 posts, etc.). The more listings acquired, the more accurate your results will be. (NB: It will stop searching for listings if there is nothing else to search through, even if you specified more listings to analyze)

## Some Issues/Shortcomings/Things to Consider
* The AllSides bias data (which they so kindly gave to me for the purposes of this project) required quite a bit of formatting (in terms of the links), because they would otherwise not be so nice to parse through.
* The bias data seems to need to be expanded, as most of my testing led to more than 50% inconclusive data.
* The way that top level domains are handled could also probably be changed, as that may be making the data more inconclusive.
* The way in which the listings are collected could be optimized, as it would be more efficient to get all of the listings in one session and then parse the results, instead of utilizing multiple sessions (but that would be an optimization in `main.py`).
* The way in which the links are checked if they have a bias rating or not could be optimized, rather than brute-forcing.
* The script is not optimized to ignore pictures or text posts.
* The script ***only*** checks the links of posts, and ***does not*** consider the title of the post, the title of the article, or the text of any comments therein.  
* The script, in general, is not written well, and can be optimized.

## LICENSE NOTICE
All code in this repository is licensed under GPLv3 ***EXCEPT FOR*** the AllSides.com Bias Ratings file (`bias-analyzer/AllSidesBiasRatings.json`), which is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License.](https://creativecommons.org/licenses/by-nc/4.0/) A copy of the license notice is also included in the file.
