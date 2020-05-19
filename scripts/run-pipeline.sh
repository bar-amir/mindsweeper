#!/bin/bash

protos="./mindsweeper/protos"
for file in "$protos"/*;
do
    if [[ -f $file ]]
    then
        python -m grpc_tools.protoc -I"$protos" --python_out="$protos"/code/ --grpc_python_out="$protos"/code/ $file
    fi
done

