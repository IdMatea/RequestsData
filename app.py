from click import command
from flask import Flask, request
from collections import Counter
from commands import * 
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys

# create the Flask app
app = Flask(__name__)


#####################################################################
all_values = {}
manager = CommandManager()

@app.route('/')
def index():
    return 'Hi, please enter your request.'


@app.route('/get')
def get():
    name = request.args.get('name')
    return all_values.get(name,'None')

@app.route('/set')
def set():
    name = request.args.get('name')
    value = request.args.get('value')
    result = manager.do(ElementSet(all_values,name,value))
    return result


@app.route('/unset')
def unset():
    name = request.args.get('name')
    result = manager.do(ElementUnset(all_values,name,None))
    return result

@app.route('/numequalto')
def numequalto():
    value = request.args.get('value')
    res = Counter(all_values.values())
    return str(res.get(value,0))

@app.route('/undo')
def undo():
    result = manager.undo()
    return result

@app.route('/redo')
def redo():
    result = manager.redo()
    return result

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
