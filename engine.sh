sudo docker run \
    --name checkin -itd \
    -v /abs/path/to/your/res:/resource \
    -h checkin \
    --restart=on-failure:10 checkin