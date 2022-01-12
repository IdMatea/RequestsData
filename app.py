import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# create the Flask app
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




#####################################################################

# @app.route('/')
# def home():
#     return 'Hello!'


# @app.route('/get')

@app.route('/set')
def set():
    name = request.args.get('name')
    value = request.args.get('value')
    return name + ' = ' + value
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