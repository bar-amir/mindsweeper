#!/bin/bash

docker run -d \
           --hostname my-rabbit \
           --name ms-mq \
           -p 5672:5672 \
           -p 15672:15672 \
           rabbitmq:3-management;

docker run -d \
            --name ms-db
            -p 27017-27019:27017-27019 \
            mongo:4.0.4


protos="./mindsweeper/protos"
for file in "$protos"/*;
do
    if [[ -f $file ]]
    then
        python -m grpc_tools.protoc -I"$protos" --python_out="$protos"/code/ --grpc_python_out="$protos"/code/ $file
    fi
done



source .env/bin/activate
python -m mindsweeper.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
python -m mindsweeper.parsers run-parser 'depth_image' 'rabbitmq://127.0.0.1:5672/'
python -m mindsweeper.parsers run-parser 'color_image' 'rabbitmq://127.0.0.1:5672/'
python -m mindsweeper.parsers run-parser 'feelings' 'rabbitmq://127.0.0.1:5672/'
python -m mindsweeper.server run-server 'rabbitmq://127.0.0.1:5672/'
python -m mindsweeper.saver run-saver 'mongodb://localhost:27017/' 'rabbitmq://127.0.0.1:5672/'
python scripts/start_over_db.py
python -m mindsweeper.client upload-sample '/home/baram/Documents/mindsweeper/sample.mind.gz'