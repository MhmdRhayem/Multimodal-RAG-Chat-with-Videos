from utils import *
from flask import Flask, request, jsonify
import os

chain = None
embedder = None
table = None

