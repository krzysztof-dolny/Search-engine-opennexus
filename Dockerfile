# Python Image
FROM python:3.11.2

WORKDIR /app

RUN apt update -y && apt install ffmpeg -y

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install pysqlite3-binary

CMD [ "python", "run.py"]