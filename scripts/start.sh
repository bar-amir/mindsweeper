# RabbitMQ
docker run -d \
           --hostname my-rabbit \
           --name some-rabbit \
           -p 5672:5672 \
           -p 15672:15672 \
           rabbitmq:3-management

# PostgreSQL
docker run -d \
           --name some-postgres \
           -p 5432:5432 \
           -e POSTGRES_PASSWORD=password \
           postgres