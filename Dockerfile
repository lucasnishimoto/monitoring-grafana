FROM python:alpine 

WORKDIR /app

COPY *.py /app/

RUN pip install --upgrade pip redis influxdb && \
apk add iputils

CMD python3 main.py 
