from bottle import Bottle, view, request

from collections import deque
import json


# App Engine ?
app = Bottle()


# This is the global, shared list of the most recent messages.
MESSAGES = deque(maxlen=20)


@app.route('/')
@view('views/index')
def index():
    #host = bottle.request.get_header('host')
    host = ''
    return dict(host=host)

@app.route('/chat')
def chat_get():
    return {'messages': list(MESSAGES)}

@app.post('/chat', method='POST')
def chat_post():
    try:
        if request.json:
            jsonMessage = request.json
        elif request.body:
            # request.body is a StringIO.
            jsonMessage = json.loads(request.body.getvalue())
        else:
            return {'status': 'ERROR', 'description': 'No message received.'}
    except ValueError as e:
        return {'status': 'ERROR', 'description': 'Could not parse JSON.'}

    if not jsonMessage:
        return {'status': 'ERROR', 'description': 'No JSON message received.'}

    MESSAGES.append({'message': jsonMessage['message']})

    return {'status': 'OK'}

# Define an handler for 404 errors.
@app.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL. (404)'
