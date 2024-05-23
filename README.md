# Running
## Debug
### Linux / MacOS

   ```commandline
   ./scripts/bash/debug.sh
   ```

### Windows
Please notice that it can be slow because of mounting Windows folder into Docker container. You can change it to named volume but it will enforce to use dev container to make changes. You can also use venv in Windows and skip docker.

   ```commandline
   .\scripts\bash\debug.bat
   ```

### Venv
#### Getting started
1. Install python3 (3.12.3 is recommended)
2. Create venv

   ```commandline
   python3 -m venv venv
   ```
3. Activate venv

   ```commandline
   # In cmd.exe
   venv\Scripts\activate.bat
   
   # In PowerShell
   venv\Scripts\Activate.ps1

   # Linux/MacOS
   source venv/bin/activate
   ```

4. Install command-line tool `ffmpeg` ([https://ffmpeg.org/download.html](https://ffmpeg.org/download.html))

5. Create `.env` file - you can just copy `template.env`. In `.env` file are credentials to development SMTP server. Emails will be truly send. 

6. Install dependencies

   ```commandline
   pip3 install -r requirements.txt
   ```

7. Replace `venv/lib/$python/site-packages/pytube/cipher.py` with `pytube/cipher.py` where `$python` is your python version e.g. `python3.11`.

#### Running
1. Run app in debug mode

   ```commandline
   python3 -m flask --app ./app run --host=0.0.0.0 --port=5000 --debug
   ```

## Release
### Linux / MacOS

   ```commandline
   ./scripts/bash/release.sh
   ```

### Windows
Please notice that it can be slow because of mounting Windows folders into Docker container. You can change it to named volumes or use linux filesystem inside Windows.

   ```commandline
   .\scripts\bash\release.bat
   ```

# Getting started with admin panel
Login with `admin@admin.admin` email and add more admins in panel to test email & code process.
