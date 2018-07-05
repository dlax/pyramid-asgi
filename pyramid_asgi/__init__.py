from asgiref.wsgi import WsgiToAsgi


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


def includeme(config):
    config.registry.setdefault(
        'protocol-router', {'http': {}, 'websocket': {}},
    )
