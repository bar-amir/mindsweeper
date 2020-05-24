#!/bin/bash

# scripts/compile-protos.sh
# docker-compose up

docker stop $(docker ps -a -q);
docker rm -vf $(docker ps -a -q)
docker rmi -f $(docker images -a -q)
sudo rm -r ./data


# sudo docker build -t ms-server .
# docker tag ms-server:latest
# docker-compose up
# docker network create ms-network
# docker run -d \
#            --name ms-rabbit \
#            --hostname ms-rabbit \
#            --net ms-network \
#            -p 5672:5672 \
#            -p 15672:15672 \
#            rabbitmq:3-management;
# docker run -d \
#            --name ms-mongodb \
#            --hostname ms-mongodb \
#            --net ms-network \
#            -p 27017-27019:27017-27019 mongo:4.0.4
#curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
#sudo apt-get install -y nodejs
# 
# docker run -d \
#            --name ms-server \
#            --hostname ms-server \
#            --net ms-network \
#            -p 8000:8000 \
#            ms-server



# source .env/bin/activate
# python -m mindsweeper.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
# python -m mindsweeper.parsers run-parser 'depth_image' 'rabbitmq://127.0.0.1:5672/'
# python -m mindsweeper.parsers run-parser 'color_image' 'rabbitmq://127.0.0.1:5672/'
# python -m mindsweeper.parsers run-parser 'feelings' 'rabbitmq://127.0.0.1:5672/'
# python -m mindsweeper.server run-server 'rabbitmq://127.0.0.1:5672/'
# python -m mindsweeper.saver run-saver 'mongodb://localhost:27017/' 'rabbitmq://127.0.0.1:5672/'
# python scripts/start_over_db.py
# python -m mindsweeper.client upload-sample '/home/baram/Documents/mindsweeper/sample.mind.gz'