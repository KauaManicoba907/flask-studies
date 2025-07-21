from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from cadastro_e_login import *
from tarefascrud import *

if __name__ == '__main__':
    app.run(debug=True)
