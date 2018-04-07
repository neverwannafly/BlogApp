#!/usr/bin/env python3
# Main Appilcation

from flask import Flask

app = Flask(__name__)

if __name__=="__main__":
    app.run(debug=True)