__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from app import app
import os

if __name__ == "__main__":
    app.run("0.0.0.0", port=os.getenv('PORT', 6969),  load_dotenv=True)
