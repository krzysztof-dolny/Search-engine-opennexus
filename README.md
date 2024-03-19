## How to run on local venv:
### 1.configure python venv
### 2.install dependencies:
```commandline
pip3 install -r requirements.txt
```
### 3.It also requires the command-line tool ffmpeg to be installed on your system
### 4. run 'run.py' file (first time might take longer)




## How to run on docker (not finnished):
### First Flask Docker Build:
```commandline
docker build -t flaskimage .
```

### First ChromaDB Image Pull:
```commandline
docker pull chromadb/chroma
```

### Run Flask App from Docker
```commandline
docker run -p 5000:5000
```

docker network create mynetwork
docker run -d --network=mynetwork --name=chromadb -p 8000:8000 -v /Users/tim/Dekstop/chroma/:/chroma/chroma chromadb/chroma
docker build -t myflaskapp .
docker run -d --network=mynetwork --name=myflaskapp -p 5000:5000 myflaskapp
