import os
from flask import Flask, request

# create the Flask app
app = Flask(__name__)




#####################################################################
all_values = {}

@app.route('/')
def index():
    return 'Hi, please enter your request.'


# @app.route('/get')

@app.route('/set')
def set():
    name = request.args.get('name')
    value = request.args.get('value')
    all_values[name] = value
    return name + " = "+ all_values[name]

# @app.route('/unset')
# @app.route('/numequalto')
# @app.route('/undo')
# @app.route('/redo')
@app.route('/end')
def end(): 
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return 'CLEANED'

#####################################################################
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(port=5000, debug=True)
