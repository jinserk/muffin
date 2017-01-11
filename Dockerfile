FROM debian:testing
MAINTAINER Jinserk Baik <jinserk.baik@gmail.com>

RUN apt update -y
RUN apt dist-upgrade -y
RUN apt install -y python3 python3-pip python3-dev build-essential

ADD . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py", "run", "--bind", "0.0.0.0:5000"]
