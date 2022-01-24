from webbrowser import Chrome
from flask import Flask, request
from collections import Counter
#from selenium import webdriver
from commands import *
from google.cloud import datastore

# Instantiates a client
datastore_client = datastore.Client()

# The kind for the new entity
kind = "Task"
# The name/ID for the new entity
name = "save"
# The Cloud Datastore key for the new entity
task_key = datastore_client.key(kind, name)

# Prepares the new entity
task = datastore.Entity(key=task_key)
task["description"] = "Buy milk"

# Saves the entity
datastore_client.put(task)

print(f"Saved {task.key.name}: {task['description']}")


# create the Flask app
app = Flask(__name__)
#####################################################################

@app.route('/')
def index():
    return 'Hi, please enter your request.'


@app.route('/get')
def get():
    name = request.args.get('name')
    data = OpenDB()
    return data["values"].get(name,'None')

@app.route('/set')
def set():
    name = request.args.get('name')
    value = request.args.get('value')
    data = OpenDB()
    result = do(ElementSet(data,name,value))
    UpdateDB(data)
    return result


@app.route('/unset')
def unset():
    name = request.args.get('name')
    data = OpenDB()
    result = do(ElementUnset(data,name,None))
    UpdateDB(data)
    return result

@app.route('/numequalto')
def numequalto():
    value = request.args.get('value')
    data = OpenDB()
    res = Counter(data["values"].values())
    return str(res.get(value,0))

@app.route('/undo')
def undo():
    data = OpenDB()
    result = undo(data)
    return result

@app.route('/redo')
def redo():
    data = OpenDB()
    result = redo(data)
    return result

@app.route('/end')
def end(): 
    data = OpenDB()
    # Iterate through the objects in the JSON and pop (remove) 
    data.clear()
    # for i in data:
    #     data.pop(i)
    UpdateDB(data)
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    # driver = webdriver.Chrome()
    # driver.get(app.route('/end'))
    # driver.close
    return 'CLEANED'


#####################################################################
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(port=5000, debug=True)
