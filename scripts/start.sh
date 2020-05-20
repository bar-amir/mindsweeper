# RabbitMQ
docker run -d \
           --hostname my-rabbit \
           --name some-rabbit \
           -p 5672:5672 \
           -p 15672:15672 \
           rabbitmq:3-management;

# PostgreSQL
docker run -d \
           --name some-postgres \
           -p 5432:5432 \
           -e POSTGRES_PASSWORD=password \
           postgres;

#Admin
docker run -d \
           --name some-pgadmin4 \
           --link some-postgres:postgres \
           -p 5050:5050 \
           fenglc/pgadmin4;

#user: pgadmin4@pgadmin.org password: admin

docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:4.0.4
