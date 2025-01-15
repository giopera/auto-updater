import os

from flask import Flask, request, jsonify
import json
import yaml

from server.utils.RequestData import RequestData

app = Flask(__name__)

repos: dict = {}
'''
The repos that are allowed and tracked by the program, where they are, the location of the cache directory for old
compiled versions and other info
'username/repo': {
    'dir': "./username/repo/",
    'url': "http://github.com/username/repo"
    'tmp_dir': 
}
'''

settings: dict = {}
'''
The settings and configurations of the server
"port": "8080"
"host": "0.0.0.0"
"tmp_dir": "/tmp/"
'''


def load_repos():
    global repos
    repos = json.load(open("settings/repos.json"))
    for key, value in repos.items():
        repos[key]['tmp_dir'] = repos[key].get('tmp_dir', f"{settings['tmp_dir']}{key}")
        repos[key]['dir'] = repos[key].get('dir', f"{settings['current_dir']}{key}")


def load_settings():
    global settings
    with open("settings.yml", "r") as file:
        settings = yaml.safe_load(file)

    settings['port'] = settings.get('port', 8080)
    settings['host'] = settings.get('host', "0.0.0.0")
    settings['tmp_dir'] = settings.get('tmp_dir', "/tmp/")
    settings['current_dir'] = f"{os.path.dirname(__file__)}/"


@app.route(f"/webhook", methods=["POST"])
def webhook_receiver():

    data = RequestData().loadData(request)

    if data.repository in repos:
        print("in")
    else:
        print(f"Received webhook for {data.repository} but it's not in the repos we are watching")

    return jsonify({'message': 'Webhook received successfully'}), 200


if __name__ == '__main__':
    load_settings()
    load_repos()
    app.run(debug=True, port=8080, host="0.0.0.0")
