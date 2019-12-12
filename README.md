# crawler
docker build -t image_crawler crawler/
docker run -it --rm -p 8080:8080 -v /c/obara/TwitterProject/crawler:/app image_crawler /bin/bash
