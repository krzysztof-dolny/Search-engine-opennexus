# Python Image
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# Copy Source Code to Container
COPY . .

# Run the app
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]