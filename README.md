# crawler develop
docker build -t image_crawler crawler/
docker run -it --rm -p 8080:8080 -v /c/obara/TwitterProject/crawler:/app image_crawler /bin/bash

# crawler deploy
docker build -t gcr.io/twitter-261302/crawler .
gcloud docker -- push gcr.io/twitter-261302/crawler
