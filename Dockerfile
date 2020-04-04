FROM python

ADD . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD flask run --host=0.0.0.0 --port=8080
