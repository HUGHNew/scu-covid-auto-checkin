FROM python:3-alpine

COPY ./DockerRes/ .

RUN pip install -r requirements.txt --no-cache-dir

# use CST
RUN apk update \
    && apk add tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

ENV maintainer hugh
ENV version 2.0
ENV ENV "/etc/profile"

WORKDIR /
# it can also set /root where is the workdir of crond

# UTC 17 - CST 1
# CST 0:30 after timezone changed
RUN echo "30	0	*	*	*	python /checkin.py >> ./cron.log &" >> /var/spool/cron/crontabs/root

RUN echo "crond" >> /etc/profile

ENTRYPOINT [ "/bin/ash" ]