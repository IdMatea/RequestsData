from abc import ABCMeta, abstractmethod


class SetOperation(object):
    __metaclass__ = ABCMeta

    def __init__(self, set_, key, value):
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
        self.set_[self.key]= self.value
        return str(self.key) + " = "+ str(self.set_.get(self.key,'None'))

    def undo(self):
        self.set_.pop(self.key,'None')
        return str(self.key) + " = "+ str(self.set_.get(self.key,'None'))

class ElementUnset(SetOperation):
    def __call__(self):
        self.set_.pop(self.key,'None')
        return str(self.key) + " = "+ str(self.set_.get(self.key,'None'))

    def undo(self):
        self.set_[self.key]= self.value
        return str(self.key) + " = "+ str(self.set_.get(self.key,'None'))

class CommandManager(object):
    def __init__(self):
        self.undo_commands = []
        self.redo_commands = []

    def push_undo_command(self, command):
        #Push the given command to the undo command stack.
        self.undo_commands.append(command)

    def pop_undo_command(self):
        # Remove the last command from the undo command stack and return it.
        # If the command stack is empty, EmptyCommandStackError is raised.

        try:
            last_undo_command = self.undo_commands.pop()
        except IndexError:
            return 'NO COMMANDS' 
        return last_undo_command

    def push_redo_command(self, command):
        #Push the given command to the redo command stack.
        self.redo_commands.append(command)

    def pop_redo_command(self):
        # Remove the last command from the redo command stack and return it.
        # If the command stack is empty, EmptyCommandStackError is raised.

        try:
            last_redo_command = self.redo_commands.pop()
        except IndexError:
            return 'NO COMMANDS'
        return last_redo_command

    def do(self, command):
        #Execute the given command. Exceptions raised from the command arenot caught.
        result = command()
        self.push_undo_command(command)
        # clear the redo stack when a new command was executed
        self.redo_commands[:] = []
        return result

    def undo(self):
        # Undo the last command. 
        # If there is no command that can be undone because n is too big
        # or because no command has been emitted yet, EmptyCommandStackError is raised.
        command = self.pop_undo_command()
        if type(command).__name__ != 'str':
            result = command.undo()
            self.push_redo_command(command)
            return result
        return command

    def redo(self):
        # Redo the last command which have been undone using the undo method. 
        # If there is no command that can be redone because n is too big or because no command has been undone yet,
        # EmptyCommandStackError is raised.
        command = self.pop_redo_command()
        if type(command).__name__ != 'str':
            result = command()
            self.push_undo_command(command)
            return result
        return command

# if __name__ == '__main__':
#     all_values = {}
#     manager = CommandManager()
#     print(manager.do(ElementSet(all_values,'a',10)),manager.undo_commands[-1])
#     #undo = []
#     #redo =[]
#     print(manager.do(ElementSet(all_values,'a',40)))
#     print(manager.undo())
#     print(manager.undo())
#     print(manager.redo())
#     print(manager.redo())
#     print(manager.undo())
#     print(manager.redo())
#     print(manager.redo())
