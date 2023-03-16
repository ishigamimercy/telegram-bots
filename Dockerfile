FROM python:3.9-slim-bullseye

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y

RUN apt-get install git  python3-pip -y

RUN pip3 install --upgrade pip

COPY requirements.txt .

RUN pip3 install -U setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","main.py"]
