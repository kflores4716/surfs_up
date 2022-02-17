# Import Flask Dependency
from flask import Flask

# Adding first Flask app instance
app = Flask(__name__)

# Creating the first route (or root)
@app.route('/')
def hello_world():
    return 'Hello world'