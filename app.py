from flask import Flask


app = Flask(__name__)
app.debug = True

from modules import api, scraper
