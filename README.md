# crawler develop
docker build -t gcr.io/twitter-261302/crawler crawler/
docker run -it --rm -p 8080:8080 -v /c/obara/TwitterProject/crawler:/app gcr.io/twitter-261302/crawler /bin/bash

# crawler deploy
docker build -t gcr.io/twitter-261302/crawler .
gcloud docker -- push gcr.io/twitter-261302/crawler

# mysql to bq
min_id = 1205748316870328320
