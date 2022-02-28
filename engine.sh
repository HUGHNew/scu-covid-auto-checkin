sudo docker run \
    --name checkin -itd \
    -v /abs/path/to/your/res:/checkin/resource \
    --restart=on-failure:10 checkin