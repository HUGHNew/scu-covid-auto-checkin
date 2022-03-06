FROM git4docker/python3-alpine-cst:1.0

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

ENV maintainer hugh
ENV version 2.0
ENV ENV "/etc/profile"

WORKDIR /
# it can also set /root where is the workdir of crond

# CST 0:30 after timezone changed
RUN echo "30	0	*	*	*	python /checkin.py >> /cron.log &" >> /var/spool/cron/crontabs/root

RUN echo "crond" >> /etc/profile

COPY ./checkin.py .

ENTRYPOINT [ "/bin/ash" ]