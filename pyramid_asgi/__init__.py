from asgiref.wsgi import WsgiToAsgi
from pyramid.exceptions import (
    ConfigurationError,
)


class PyramidWsgiToAsgi(WsgiToAsgi):
    """Extends the WsgiToAsgi wrapper to look for ASGI consumer registered in
    Pyramid's registry (under "protocol-router" key).
    """

    def __call__(self, scope, **kwargs):
        protocol = scope["type"]
        path = scope["path"]
        protocol_router = self.wsgi_application.registry['protocol-router']
        try:
            consumer = protocol_router[protocol][path]
        except KeyError:
            return super().__call__(scope, **kwargs)
        return consumer(self.wsgi_application, scope)


def add_consumer(config, consumer, protocol, path):
    protocol_router = config.registry['protocol-router']
    try:
        routes = protocol_router[protocol]
    except KeyError:
        raise ConfigurationError(
            "unknown '{}' protocol (acceptable values are: {}".format(
                protocol, ', '.join(protocol_router.keys()))
        )

    def register():
        routes[path] = consumer

    config.action('asgi.{}[{}]'.format(protocol, path), register)


def includeme(config):
    config.registry.setdefault(
        'protocol-router', {'http': {}, 'websocket': {}},
    )
    config.add_directive('add_consumer', add_consumer)
