from flask import Blueprint
from slackify.dispatcher import Command, Dispatcher

bp = Blueprint('slack', __name__, url_prefix='/slack')


class FlackBlueprint(Blueprint):


    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)
        print(self.url_prefix)
        self.matchers = []


    def command(self, func=None, **options):
        """A decorator that is used to register a function as a command handler.

           It can be used as a plain decorator or as a parametrized decorator factory.
           This does the same as `add_command_handler`

        Usage:
            >>>@command
            >>>def hola():
            >>>    print('hola', kwargs)


            >>>@command(name='goodbye')
            >>>def chau():
            >>>    print('chau', kwargs)
        """
        def decorate(func):
            command = options.pop('name', func.__name__)
            rule = f'/{command}' if not command.startswith('/') else command
            options['methods'] = ('GET', 'POST')
            self.add_url_rule(rule, command, func, **options)
            self.matchers.append(Command(command, self.name))
            return func

        used_as_plain_decorator = bool(func)
        if used_as_plain_decorator:
            return decorate(func)
        else:
            return decorate
