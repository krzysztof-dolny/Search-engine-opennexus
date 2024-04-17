from app import app
import os
from dotenv import load_dotenv

# If file is called directly called, then run the app on the PORT provided defined in ENV or use '6969'.
if __name__ == "__main__":
    app.run("0.0.0.0", port=os.getenv('PORT', 6969), load_dotenv=True)
