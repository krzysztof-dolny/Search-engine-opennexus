## Running
### Local venv
1. Configure Python venv.
2. Install dependencies:

   ```commandline
   pip3 install -r requirements.txt
   ```

3. It also requires the command-line tool `ffmpeg` to be installed on your system.
4. Create `.env` file - you can just copy `template.env`. In `.env` file are credentials to development SMTP server. Emails will be truly send. 
5. Run `run.py` file (first time might take longer).
6. Login with `admin@admin.admin` email and add more admins in panel to test email & code process.

### Docker
1. First Flask Docker Build:

   ```commandline
   docker build -t flaskimage .
   ```

2. First ChromaDB Image Pull:

   ```commandline
   docker pull chromadb/chroma
   ```

3. Run Flask App from Docker.

   ```commandline
   docker run -p 5000:5000
   docker network create mynetwork
   docker run -d --network=mynetwork --name=chromadb -p 8000:8000 -v /Users/tim/Dekstop/chroma/:/chroma/chroma chromadb/chroma
   docker build -t myflaskapp .
   docker run -d --network=mynetwork --name=myflaskapp -p 5000:5000 myflaskapp
   ```
