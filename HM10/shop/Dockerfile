FROM python:3.10

WORKDIR code/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 gcc python3-dev python3-pip cython3
RUN apt-get -y install python3-numpy python3-scipy
RUN apt install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .
RUN ls


ENTRYPOINT ["/code/entrypoint.sh"]
