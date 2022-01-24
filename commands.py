from abc import ABCMeta, abstractmethod
import os,json



def OpenDB():
    try:
        with open('DataStore.json', "rt") as f:
            if os.path.getsize('DataStore.json') > 0:
                db = json.load(f)
            else:
                db={"values":{},"history":{},"undo_commands":[],"redo_commands":[]}
        f.close()
    except IOError:
        # Could not read file, starting from scratch
        db={"values":{},"history":{},"undo_commands":[],"redo_commands":[]}
    return db

def UpdateDB(db):
    with open('DataStore.json', "wt") as f:
        json.dump(db, f)
    f.close()

            

class SetOperation(object):
    __metaclass__ = ABCMeta

    def __init__(self, set_,key, value):
        self.set_ = set_
        self.key = key
        self.value = value

    @abstractmethod
    def __call__(self):
        return

    @abstractmethod
    def undo(self):
        return


class ElementSet(SetOperation):
    def __call__(self):
        self.set_["values"][self.key]= self.value
        # manage history list for each key
        if self.key in self.set_["history"]:
            self.set_["history"][self.key].append(self.value)
        else:
            self.set_["history"].update({self.key:[self.value]})
        # manage command's history by insert the command details 
        self.set_["undo_commands"].append(['set',self.key,self.value])
        return str(self.key) + " = "+ str(self.set_["values"].get(self.key,'None'))

    def undo(self):
        # remove last value from current key and take last val
        # if non exist - then unset
        last_value = 0
        try:
            self.set_["history"][self.key].pop()
            last_value = self.set_["history"][self.key][-1]
            self.set_["values"][self.key]= last_value
            if last_value == None:
                self.set_["values"].pop(self.key,'None')
        except IndexError:
            'NO COMMANDS'
        return str(self.key) + " = "+ str(self.set_["values"].get(self.key,'None'))

class ElementUnset(SetOperation):
    def __call__(self):
        self.set_["values"].pop(self.key,'None')
        self.set_["history"][self.key].append(None)
        self.set_["undo_commands"].append(['unset',self.key])
        return str(self.key) + " = "+ str(self.set_["values"].get(self.key,'None'))

    def undo(self):
        try:
            self.set_["history"][self.key].pop()
            last_value = self.set_["history"][self.key][-1]
            self.set_["values"][self.key]= last_value
        except IndexError:
            return 'NO COMMANDS'
        return str(self.key) + " = "+ str(self.set_["values"].get(self.key,'None'))

def do(command):
    #Execute the given command. Exceptions raised from the command arenot caught.
    data = command()
    return data

def undo(data):
    # Undo the last command. 
    # If there is no command NO COMMANDS is raised.
    try:
        command = data["undo_commands"].pop()
        # pop the last undo into redo
        data["redo_commands"].append(command)
    except IndexError:
        return 'NO COMMANDS'
    if command[0] == 'set':
        result = ElementSet(data,command[1],command[2]).undo()
    elif command[0] == 'unset':
        result = ElementUnset(data,command[1],None).undo()
    else:
        return 'Something went wrong!'
    return result

def redo(data):
    # Redo the last command which have been undone using the undo method. 
    # If there is no command that can be redone because no command has been undone yet,
    # NO COMMANDS is raised.
    try:
        command = data["redo_commands"].pop()
        data["undo_commands"].append(command)
    except IndexError:
        return 'NO COMMANDS'
    if command[0] == 'set':
        result = ElementSet(data,command[1],command[2])()
    elif command[0] == 'unset':
        result = ElementUnset(data,command[1],None)()
    else:
        return 'Something went wrong!'
    return result


# #for testing:
# if __name__ == '__main__':
#     all_values = {"values":{},"history":{},"undo_commands":[],"redo_commands":[]}
#     manager = CommandManager()
#     print(manager.do(ElementSet(all_values,'a',10)))
#     print(manager.do(ElementSet(all_values,'b',140)))
#     print(manager.do(ElementUnset(all_values,'a',None)))
#     print(manager.do(ElementSet(all_values,'a',2)))
#     print(manager.do(ElementSet(all_values,'a',321)))
#     print(manager.do(ElementSet(all_values,'b',3556)))
#     print(all_values)
#     print(manager.undo(all_values))
#     print(all_values)
#     print(manager.undo(all_values))
#     print(all_values)
#     print(manager.undo(all_values))
#     print(all_values)
#     print(manager.undo(all_values))
#     print(all_values)
#     print(manager.undo(all_values))
#     print(all_values)
#     print(manager.undo(all_values))
#     print(all_values)
#     print(manager.undo(all_values))
#     print(all_values)
#     print(manager.redo(all_values))
#     print(all_values)
#     print(manager.redo(all_values))
#     print(all_values)
#     print(manager.undo(all_values))
#     print(all_values)
#     print(manager.redo(all_values))
#     print(all_values)
#     # print(all_values["redo_commands"].pop() if all_values["redo_commands"] else 'Empty!')
#     exp = [{"ElementSet(all_values,'b',10)":'set b'},{"ElementSet(all_values,'a',10)":'set a'},{"ElementSet(all_values,'a',40)":'set a'}]
#     current = exp.pop()
#     if(list(current.values())[-1] == list(exp[-1].values())[-1]):
#         print(True)
    
#     print(all_values)

