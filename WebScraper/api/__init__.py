from flask import Flask, request

app = Flask(__name__)

from .routes import main_route
