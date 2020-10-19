# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# ***Important: still, need to install "crypto-news-api" package from PyPI first!

# first, activate cryptoalgowheel conda environment
# then: /anaconda3/envs/cryptoalgowheel/bin/pip install crypto-news-api


# %%
from crypto_news_api import CryptoControlAPI

import numpy as np
import pandas as pd
import json
from datetime import datetime


# %%
api = CryptoControlAPI("39b252536476db3482bab04acea666bc")

# %% [markdown]
# #### get top news (languages can be changed)

# %%
def top_news(api, language="en"):
    topnews = api.getTopNews(language)
    topnews = pd.DataFrame(topnews)
    topnews.to_csv("./top_news.csv", index=False)

top_news(api)

# %% [markdown]
# #### get latest news (languages can be changed)

# %%
def latest_news(api, language="en"):
    latest_news = api.getLatestNews(language)
    latest_news = pd.DataFrame(latest_news)
    latest_news.to_csv("./latest_news.csv", index=False)

latest_news(api, "ru")

# %% [markdown]
# #### get top news by category for "en" news (for "en" news currently 6 main categories: "Analysis", "Blockchain", "Exchanges", "Government", "Mining & ICOs" plus 1 "general" categories) (for all other languages than "en", all news classified as "general", so not focused here)
# 

# %%
def top_news_by_category(api, language="en"):
    topnews_by_cat = api.getTopNewsByCategory(language)
    for k,v in topnews_by_cat.items():
        current = pd.DataFrame(v)
        current.to_csv("./top_news_"+str(k)+".csv", index=False)

top_news_by_category(api)
top_news_by_category(api, "jp")

# %% [markdown]
# #### get top news for a specific coin

# %%
def top_news_by_coin(api, coin, language="en"):
    topnews_coin = api.getTopNewsByCoin(coin, language)
    topnews_coin = pd.DataFrame(topnews_coin)
    topnews_coin.to_csv("./top_news_"+str(coin)+".csv", index=False)

top_news_by_coin(api, "bitcoin")

# %% [markdown]
# #### get top news for a specific coin

# %%
def latest_news_by_coin(api, coin, language="en"):
    latest_news_coin = api.getLatestNewsByCoin(coin, language)
    latest_news_coin = pd.DataFrame(latest_news_coin)
    latest_news_coin.to_csv("./latest_news_"+str(coin)+".csv", index=False)

latest_news_by_coin(api, "bitcoin")

# %% [markdown]
# #### get top reddit posts for a specific coin

# %%
def top_reddit_by_coin(api, coin, language="en"):
    top_reddit_coin = api.getTopRedditPostsByCoin(coin, language)
    top_reddit_coin = pd.DataFrame(top_reddit_coin)
    top_reddit_coin.to_csv("./top_reddit_"+str(coin)+".csv", index=False)

top_reddit_by_coin(api, "ripple")

# %% [markdown]
# #### get latest reddit posts for a specific coin

# %%
def latest_reddit_by_coin(api, coin, language="en"):
    latest_reddit_coin = api.getLatestRedditPostsByCoin(coin, language)
    latest_reddit_coin = pd.DataFrame(latest_reddit_coin)
    latest_reddit_coin.to_csv("./latest_reddit_"+str(coin)+".csv", index=False)

latest_reddit_by_coin(api, "ripple")

# %% [markdown]
# #### get top tweets for a specific coin

# %%
def top_tweets_by_coin(api, coin, language="en"):
    top_tweets_coin = api.getTopTweetsByCoin(coin, language)
    top_tweets_coin = pd.DataFrame(top_tweets_coin)
    top_tweets_coin.to_csv("./top_tweets_"+str(coin)+".csv", index=False)

top_tweets_by_coin(api, "eos")

# %% [markdown]
# #### get latest tweets for a specific coin

# %%
def latest_tweets_by_coin(api, coin, language="en"):
    latest_tweets_coin = api.getLatestTweetsByCoin(coin, language)
    latest_tweets_coin = pd.DataFrame(latest_tweets_coin)
    latest_tweets_coin.to_csv("./latest_tweets_"+str(coin)+".csv", index=False)

latest_tweets_by_coin(api, "eos")

# %% [markdown]
# #### get a top combined feed for a specific coin

# %%
def top_feed_by_coin(api, coin, language="en"):
    top_feed_coin = api.getTopFeedByCoin(coin, language)
    top_feed_coin = pd.DataFrame(top_feed_coin)
    top_feed_coin.to_csv("./top_feed_"+str(coin)+".csv", index=False)

top_feed_by_coin(api, "neo")

# %% [markdown]
# #### get a latest combined feed for a specific coin

# %%
def latest_feed_by_coin(api, coin, language="en"):
    latest_feed_coin = api.getLatestFeedByCoin(coin, language)
    latest_feed_coin = pd.DataFrame(latest_feed_coin)
    latest_feed_coin.to_csv("./latest_feed_"+str(coin)+".csv", index=False)

latest_feed_by_coin(api, "neo")

# %% [markdown]
# #### get top items - reddits/tweets/news_articles (separated) - for a specific coin

# %%
def top_items_by_coin(api, coin, language="en"):
    top_items_coin = api.getTopItemsByCoin(coin, language)
    top_items_coin = pd.DataFrame(top_items_coin)
    top_items_coin.to_csv("./top_items_"+str(coin)+".csv", index=False)

top_items_by_coin(api, "litecoin")

# %% [markdown]
# #### get latest items - reddits/tweets/news_articles (separated) - for a specific coin

# %%
def latest_items_by_coin(api, coin, language="en"):
    latest_items_coin = api.getLatestItemsByCoin(coin, language)
    latest_items_coin = pd.DataFrame(latest_items_coin)
    latest_items_coin.to_csv("./latest_items_"+str(coin)+".csv", index=False)

latest_items_by_coin(api, "litecoin")

# %% [markdown]
# #### get all details about a specific coin (links, description, subreddits, twitter etc.)

# %%
def coin_details(api, coin):
    coin_details = api.getCoinDetails(coin)
    print("Description:", coin_details["description"])
    print("Gitrepos:", coin_details["gitrepos"])
    print("Useful extra links:")
    display(pd.DataFrame(coin_details["links"]))
    print("Subreddits:", coin_details["subreddits"])
    print("TwitterUsernames:", coin_details["twitterUsernames"])

coin_details(api, "ethereum")


# %%



