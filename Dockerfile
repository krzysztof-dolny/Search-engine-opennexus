# Python Image
FROM python:3.12.3-bookworm

WORKDIR /app

RUN apt update -y && apt install ffmpeg -y

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY pytube/cipher.py /usr/local/lib/python3.12/site-packages/pytube/cipher.py

COPY template.env .env

COPY static ./static
COPY modules ./modules
COPY templates ./templates
COPY app.py .
COPY release.py .
COPY run.sh .

CMD [ "./run.sh"]