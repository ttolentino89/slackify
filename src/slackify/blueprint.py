import logging
from flask import Blueprint, _request_ctx_stack
from slackify.dispatcher import Command, Dispatcher


logger = logging.getLogger(__name__)

class FlackBlueprint(Blueprint):


    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)
        self._endpoint = self.url_prefix or '/'
        self._bind_main_endpoint(self.url_prefix)
        self.before_request(self._redirect_requests)
        self.dispatcher = Dispatcher()
        self.matchers = []

    def _redirect_requests(self):
        request = _request_ctx_stack.top.request
        if request.routing_exception is not None:
            self.raise_routing_exception(request)

        if request.method == 'GET' or request.path != self._endpoint:
            return

        try:
            endpoint = self.dispatcher.match(request)
        except StopIteration:
            logger.info('No handler matched this request')
            return
        except Exception as e:
            logger.exception('Something bad happened.')
            return

        rule = request.url_rule
        rule.endpoint = endpoint

    def _bind_main_endpoint(self, url_prefix):
        self.add_url_rule('/', f'__{self.name}', lambda: f'{self.name} Home', methods=('GET', 'POST'))


    def command(self, func=None, **options):
        """A decorator that is used to register a function as a command handler.

           It can be used as a plain decorator or as a parametrized decorator factory.

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
            self.add_url_rule(rule, command, func, **options)
            self.dispatcher.add_matcher(Command(command))
            return func

        used_as_plain_decorator = bool(func)
        if used_as_plain_decorator:
            return decorate(func)
        else:
            return decorate
