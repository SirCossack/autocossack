"""
Place where I'll hopefully be able to store bot commands

Not sure whether I want to continue using commands as a class as it's messy.
Need to rethink how I want to manage it in the best way possible.

TO DO:
-command counters can't get reset on restarting the bot (database?)
-multiple channels should have the same command but different counts (database?)

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
        for i in params[2:]:
            if i.startswith('message='):
                message = i[8:]
            elif i.startswith('function='):
                function = i[9:]
            elif i.startswith('count='):
                count = int(i[6:])
            elif i.startswith('ran_range='):
                 ran_range = i[10:]
        try:
            Command(name, message, function, count, ran_range)
            return "Command added."
        except: #bare except block yada yada
            return "Error - could not add command."


    @staticmethod
    def edit(message):
        pass

    commands = {'add':add, "edit":edit}
    def __init__(self, name: str, message: Optional[str] = None, function: Optional[str] = None, count: Optional[int] = None, ran_range: Optional[list[int,int]] = None, *params):
        """
        :param name: the name of the command, maybe it'll come in handy, dunno yet
        :param message: message to be sent out to chat
        :param function: what the function does (for example increase self.counter, ban a person etc)
        :param count: a counter that the command keeps track of
        :param ran_range: range in which the command randomizes values (len = 2)
        :param params: does nothing yet
        """
        self.name = name
        self.message = message
        if function: self.function = Command._parse_function(function)
        else: self.function = Command._pass
        self.count = count
        self.ran_range = ran_range
        Command.commands[self.name] = self

    @staticmethod
    def _pass():
        pass

    def __call__(self, *args, **kwargs):
        self.function()
        if self.message: return self._parse_message()  #this is probably unsafe, i'll figure something out later since i'm the only one using the bot now

    def show(self):
        print(self.name, self.message, self.count, self.function)

    def _parse_function(func):
        def function():
            print('xd')
        return function

    def _parse_message(self):
        return self.message


# !add counter count=0 message="The count is {count}" function="count = count + 1"


counter = Command(name='!counter', message='The count is {self.count}.format(self.count)', count=1, function = None)
#counter.show()
#print(counter())
print(Command.add("add deth count=0 message='deth' function=None ran_range=(0,10)"))

print(Command.commands["deth"].count)