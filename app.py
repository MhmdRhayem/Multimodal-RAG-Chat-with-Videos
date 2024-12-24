from utils import *
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
chain = None
embedder = None
table = None

