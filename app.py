from os import getenv
from flask import Flask, session
import secrets


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes