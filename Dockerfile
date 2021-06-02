FROM python:3 AS build
MAINTAINER Patrick Higgins "phiggins@cs.uoregon.edu"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

# cryptography and openssl required for https service
RUN pip install cryptography pyopenssl
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r app/requirements.txt

FROM build
COPY . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["app/bank.py"]
