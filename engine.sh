res=/abs/path/to/your/res
if [ -d $res ];then
    sudo docker run \
        --name checkin -itd \
        -v $res:/resource \
        -h checkin \
        --restart=on-failure:10 checkin
else
    echo -e "\033[031mCORRECT resource needed! \033[0m"
fi