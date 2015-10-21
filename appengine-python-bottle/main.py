from bottle import Bottle, view

app = Bottle()

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
@view('views/index')
def index(name='World'):
    return dict(name=name)

# Define an handler for 404 errors.
@app.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.'
