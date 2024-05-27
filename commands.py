"""
Place where I'll hopefully be able to store bot commands

Not sure whether I want to continue using commands as a class as it's messy.
Need to rethink how I want to manage it in the best way possible.

TO DO:
-command counters can't get reset on restarting the bot (database?)
-multiple channels should have the same command but different counts (database?)
-commands should take parameters custom parameters (**kwargs should do the trick?)
-adding time-based commands

"""
from typing import *


class Command:
    @staticmethod
    def add(message: str) -> str:
        """
        A command to add another commands in chat. It's ugly, i hate it, I'm not even sure it works
        :param message: The message from chat the bot will receive
        :return: a string saying weather a command was successfully created
        """
        #I know the implementation is horrible, not-scalable etc but I want to get this to work asap
        params = message.split()
        name = params[1]
        message = None
        function = None
        count = None
        ran_range = None
        inum = 2
        for i in range(2,len(params)):
            if params[i].startswith('message='):
                message = params[i][8:]
                counter = i+1
                while counter < len(params):
                    message = message + ' ' + params[counter]
                    if "'" in params[counter]:
                        break
                    counter += 1

            elif params[i].startswith('function='):
                function = params[i][9:]
                counter = i + 1
                while counter < len(params):
                    function = function + ' ' + params[counter]
                    if r"'" in params[counter]:
                        break
                    counter += 1
            elif params[i].startswith('count='):
                count = int(params[i][6:])
            elif params[i].startswith('ran_range='):
                 ran_range = params[i][10:]
            inum += 1
        try:
            Command(name, message, function, count, ran_range)
            return "Command '{}' added.".format(name)
        except: #bare except block yada yada
            return "Error - could not add command."


    @staticmethod
    def edit(message):
        pass


    @staticmethod
    def _pass():
        pass

    def __call__(self, *args, **kwargs):
        #this is probably unsafe, i'll figure something out later since i'm the only one using the bot now
        exec(self._parse_function(),{"__builtins__": {"print":print}, "Command":Command, "Command.commands":Command.commands},{"self":self})
        if self.message: return self._parse_message()

    def show(self):
        print(self.name, self.message, self.count, self.function)

    def _parse_function(self) -> str:
        """
        Takes self.function from the Command object and converts it from unparsed state (for example: '{count} = {count} + 1.) to a parsed state ('self.count = self.count + 1.)
        Also changes 'xxxxx.count' into 'Command.commands['xxxxx'].count, so values from other commands are also available.
        This is then put into exec() in Command.__call__
        :return: a parsed string
        """
        output = ''
        bracket = False
        variables = []
        for char in self.function:
            if bracket:
                if char == '}':
                    bracket = False
                    variables.append(variable)
                    output += char
                else:
                    variable += char
                continue

            if char == '{':
                bracket = True
                variable = ''
                output += char

            else:
                output += char

        for i in range(len(variables)):
            if "." in variables[i]:
                idx = variables[i].index(".")
                variables[i] = "Command.commands['{}'].{}".format(variables[i][:idx], variables[i][idx+1:])
            else:
                variables[i] = "self." + variables[i]
        output = output.format(*[i for i in variables])
        return output
        def func(*params):
            for char in output:
                if
            return output

    def _parse_message(self) -> str:
        """
        Takes self.message from the Command object and converts it from unparsed state (for example: 'The count is {count}.) to a parsed state ('The count is 6.)
        :return: a parsed string
        """
        output = ''
        bracket = False
        variables = []
        for char in self.message:
            if bracket:
                if char == '}':
                    bracket = False
                    variables.append(variable)
                    output += char
                else:
                    variable += char
                continue

            if char == '{':
                bracket = True
                variable = ''
                output += char

            else:
                output += char
        for i in range(len(variables)):
            if "." in variables[i]:
                idx = variables[i].index(".")
                variables[i] = "Command.commands['{}'].{}".format(variables[i][:idx], variables[i][idx+1:])
            else:
                variables[i] = "self." + variables[i]
        output = output.format(*[eval(i, {"Command":Command}, {'self': self}) for i in variables])
        return output

    commands = {'add':add, "edit":edit, "show": show}


    def __init__(self, name: str, message: Optional[str] = None, function: Optional[str] = None, count: Optional[int] = None, ran_range: Optional[list[int,int]] = None, **params):
        """
        :param name: the name of the command, maybe it'll come in handy, dunno yet
        :param message: message to be sent out to chat
        :param function: what the function does (for example increase self.counter, ban a person etc)
        :param count: a counter that the command keeps track of
        :param ran_range: range in which the command randomizes values (len = 2)
        :param params: does nothing yet
        """
        self.name = name
        if message: self.message = message.strip("'")
        else: self.message = ""
        if function: self.function = function.strip("'")
        else: self.function = Command._pass
        self.count = count
        self.ran_range = ran_range
        Command.commands[self.name] = self
        self.params = params



print(Command.add("!add test count=2 message=print('hello my name is {count}')"))
print(Command.commands['test'])
print(Command.commands['test']())