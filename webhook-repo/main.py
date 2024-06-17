from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['github_events']
collection = db['events']


@app.route('/webhook', methods=['POST'])
def respond():
    data = request.json
    print(data)
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        if 'commits' not in data or not data['commits']:
            return 'No commits in the request', 400

        for commit in data['commits']:
            event = {
                'request_id': commit['id'],
                'author': data['sender']['login'],
                'action': event_type,
                'branch': data['ref'].split('/')[-1],  # Get the branch name from 'ref'
                'timestamp': datetime.datetime.now()
            }

        event['message'] = f"{event['author']} pushed to {event['branch']} on {event['timestamp']}"

    elif event_type == 'pull_request':
        event = {
            'request_id': data['pull_request']['id'],
            'author': data['sender']['login'],
            'action': event_type,
            'from_branch': data['pull_request']['head']['ref'],
            'to_branch': data['pull_request']['base']['ref'],
            'timestamp': datetime.datetime.now()
        }

        event[
            'message'] = f"{event['author']} submitted a pull request from {event['from_branch']} to {event['to_branch']} on {event['timestamp']}"

    elif event_type == 'pull_request_review':
        event = {
            'request_id': data['review']['id'],
            'author': data['sender']['login'],
            'action': event_type,
            'pull_request_id': data['pull_request']['id'],
            'review_state': data['review']['state'],
            'timestamp': datetime.datetime.now()
        }

        event[
            'message'] = f"{event['author']} {event['review_state']} the pull request {event['pull_request_id']} on {event['timestamp']}"
    collection.insert_one(event)
    print(event['message'])

    return '', 200


@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort('timestamp', -1))
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
