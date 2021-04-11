# crawler develop
docker build -t gcr.io/twitter-261302/crawler .
docker run -it --rm -p 8080:8080 -v c:/obara/TwitterProject/crawler:/app gcr.io/twitter-261302/crawler /bin/bash

# crawler deploy
docker build -t gcr.io/twitter-261302/crawler .
# gcloud docker -- push gcr.io/twitter-261302/crawler # deprecated
docker image push gcr.io/twitter-261302/crawler:latest

# reference
## table
### timeline
[
    {
        "name": "id",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "at_created",
        "type": "DATETIME",
        "mode": "REQUIRED"
    },
    {
        "name": "screen_name",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "text",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "by_year_month",
        "type": "INTEGER",
        "mode": "REQUIRED"
    }
]
### trend_samples
[
    {
        "name": "id",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "keyword",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "screen_name",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "retweet_count",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "text",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "at_created",
        "type": "DATETIME",
        "mode": "REQUIRED"
    },
    {
        "name": "at_crawled",
        "type": "DATETIME",
        "mode": "REQUIRED"
    }
]

### status
{"created_at": "Sat Feb 22 06:36:58 +0000 2020", "favorite_count": 18, "hashtags": [], "id": 1231105583467466752, "id_str": "1231105583467466752", "lang": "ja", "media": [{"display_url": "pic.twitter.com/OQPkm8eoo3", "expanded_url": "https://twitter.com/alpaka/status/1231105583467466752/photo/1", "id": 1231105578597904385, "media_url": "http://pbs.twimg.com/media/ERXEAEVUcAEibdW.jpg", "media_url_https": "https://pbs.twimg.com/media/ERXEAEVUcAEibdW.jpg", "sizes": {"large": {"h": 360, "resize": "fit", "w": 298}, "medium": {"h": 360, "resize": "fit", "w": 298}, "small": {"h": 360, "resize": "fit", "w": 298}, "thumb": {"h": 150, "resize": "crop", "w": 150}}, "type": "photo", "url": "https://t.co/OQPkm8eoo3"}], "retweet_count": 9, "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>", "text": "\u5197\u8ac7\u306f\u3068\u3082\u304b\u304f\u3001\u6c11\u9593\u306fBCP\u306b\u6cbf\u3063\u3066\u52d5\u3044\u3066\u308b\u3051\u3069\u3001\u56fd\u3068\u3044\u3046\u304b\u5c11\u306a\u304f\u3068\u3082\u539a\u52b4\u7701\u306fBCP\u3059\u3089\u306a\u3044\u30af\u30bd\u7d44\u7e54\u3060\u3068\u3044\u3046\u306e\u304c\u30cf\u30c3\u30ad\u30ea\u3057\u305f\u308f\u3051\u3067\u3001\u9632\u75ab\u4efb\u305b\u3089\u3093\u306a\u3044\u611f\u3042\u308a\u307e\u3059\u306d\u2026 https://t.co/OQPkm8eoo3", "urls": [], "user": {"created_at": "Mon Apr 30 15:19:10 +0000 2007", "description": "\u611b\u77e5\u822a\u7a7a\u6a5f\u306e\u662d\u548c19\u5e749\u6708\u671f\u306e\u55b6\u696d\u5831\u544a\u66f8\u3092\u63a2\u3057\u3066\u3044\u307e\u3059\u3002\u308d\u304f\u308d\u304f\u524d\u5f8c\u306e\u6587\u8108\u8aad\u307e\u305a\u306b\u5f15\u7528RT\u3059\u308b\u3084\u3064\u306f\u30d6\u30ed\u30c3\u30af\u3059\u308b\u3053\u3068\u306b\u3057\u307e\u3057\u305f", "favourites_count": 11860, "followers_count": 8487, "following": true, "friends_count": 4924, "id": 5656572, "id_str": "5656572", "listed_count": 287, "location": "\u6a2a\u9808\u8cc0\u93ae\u5b88\u5e9c\uff3b\u91ce\u5206\u63d0\u7763\uff3d", "name": "\u9280\u9aea\u63a8\u9032\u6d3e", "profile_background_color": "F5F5F5", "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", "profile_banner_url": "https://pbs.twimg.com/profile_banners/5656572/1571708260", "profile_image_url": "http://pbs.twimg.com/profile_images/1142984950435606528/kPWbClZU_normal.png", "profile_image_url_https": "https://pbs.twimg.com/profile_images/1142984950435606528/kPWbClZU_normal.png", "profile_link_color": "4782B4", "profile_sidebar_border_color": "FFFFFF", "profile_sidebar_fill_color": "F5F5F5", "profile_text_color": "708191", "screen_name": "alpaka", "statuses_count": 99177}, "user_mentions": []}