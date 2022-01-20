from click import command
from flask import Flask, request, render_template
from collections import Counter
from commands import ElementSet,ElementUnset,CommandManager 
import json



# create the Flask app
app = Flask(__name__)

#####################################################################
manager = CommandManager()
all_values ={}

@app.route('/')
def index():
    return 'Hi, please enter your request.'


@app.route('/get')
def get():
    name = request.args.get('name')
    return all_values.get(name,'None')

@app.route('/set')
def set():
    with open('DataStore.json','r+') as f:
        all_values = json.load(f)
        name = request.args.get('name')
        value = request.args.get('value')
        result = manager.do(ElementSet(all_values,name,value))
        json.dump(all_values, f)
        f.close()
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
#     import json
# obj = json.load(open("new_pandas.json"))

# # Iterate through the objects in the JSON and pop (remove)
# # the obj once we find it.
# for i in range(len(obj)):
#     path = ["000000000036.jpg","000000000049.jpg","000000000077.jpg"]

#     for j in path:
        
#         if obj[i]["path"] == j:
#             obj.pop(i)
#             break


# # Output the updated file with pretty JSON
# open("updated-file.json", "w").write(
#     json.dumps(obj)
# )


#####################################################################
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(port=5000, debug=True)
