import re
from datetime import datetime
import git
import subprocess

from flask import Flask, request
from flask.wrappers import Response

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask2!"


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

@app.route('/update1', methods=['POST'])
def webhook():
        if request.method == 'POST':
            repo = git.Repo('./hello-app2')
            origin = repo.remotes.origin
            repo.create_head('main',origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

@app.route('/update', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Pull changes from the GitHub repo
        subprocess.run(['git', '-C', './hello-app2', 'pull'])
        # Restart the app to load the new code
        subprocess.run(['touch', '/var/www/greenmangroup_pythonanywhere_com_wsgi.py'])
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400