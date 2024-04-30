"""
Place where I'll hopefully be able to store bot commands

Not sure wether I want to continue using commands as a class as it's messy.
Need to rethink how I want to manage it in the best way possible.

TO DO:
-command counters can't get reset on restarting the bot (possibly store values/counters in external file)
-multiple channels should have the same command but different counts (class, but defined in a better way?)

"""
from typing import *


class Command:
    def _counter(self):
        ret = self.count
        self.count += 1
        return "The count is {}".format(ret)
    def __init__(self,
        user_ids: list[str],
        name: str,
        on_call: object,
        count: Union[int, None] = None,
        ran_range: Union[list[int, int], None] = None,
        *params):
        """

        :param user_ids: list of user ID's for which the command should be accessible
        :param count: a counter that the command keeps track of
        :param ran_range: range in which the command randomizes values (len = 2)
        :param params:
        :param name:
        :param on_call:
        """
        self.name = name
        self.on_call = on_call
        self.user_ids = user_ids
        if count != None:
            self.count = count
        if ran_range:
            self.ran_range = ran_range
        if params:
            self.params = params
    def __call__(self, *args, **kwargs):
        return self.on_call(self)

counter = Command(['slenderkozak'],'counter', on_call=Command._counter, count=0)

