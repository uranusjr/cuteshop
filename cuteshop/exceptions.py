from __future__ import unicode_literals
from .utils import python_2_unicode_compatible


@python_2_unicode_compatible
class CommandError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


@python_2_unicode_compatible
class SpecError(Exception):

    def __init__(self, name, verb):
        self.name = name
        self.verb = verb

    def __str__(self):
        return 'Unable to {verb} specification for `{name}`'.format(
            verb=self.verb,
            name=self.name,
        )
