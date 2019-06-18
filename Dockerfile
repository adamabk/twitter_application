FROM python:3.7-alpine

RUN apk update && apk add build-base libffi-dev linux-headers postgresql-dev

RUN mkdir -p /usr/src/app

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

CMD ["python3", "./fetch.py", "--user=mta"]
