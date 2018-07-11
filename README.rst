Pyramid ASGI
============

.. image:: https://travis-ci.org/dlax/pyramid-asgi.svg?branch=master
    :target: https://travis-ci.org/dlax/pyramid-asgi

Getting Started
---------------

`pyramid_asgi` provides a wrapper to transform Pyramid WSGI applications into
ASGI applications. It also provides configurator methods to register ASGI
consumers.

Here is a simple example that defines a wrapped Pyramid application using
`pyramid_asgi.PyramidWsgiToAsgi` and registers a "websocket" consumer under
the ``/ws`` route path.

.. code-block:: python

    from asgiref.wsgi import WsgiToAsgiInstance
    from pyramid.config import Configurator
    from pyramid_asgi import PyramidWsgiToAsgi


    class WebsocketConsumer(WsgiToAsgiInstance):
        """ASGI consumer for websocket protocol."""

        async def __call__(self, receive, send):
            while True:
                message = await receive()
                if message["type"] == "websocket.connect":
                    await send({"type": "websocket.accept"})
                if message["type"] == "websocket.receive":
                    text = message.get("text")
                    if text:
                        await send({"type": "websocket.send",
                                    "text": text})


    def main(global_config, **settings):
        config = Configurator(settings=settings)
        config.scan()
        config.include('pyramid_asgi')
        config.add_consumer(WebsocketConsumer, 'websocket', '/ws')
        app = config.make_wsgi_app()
        return PyramidWsgiToAsgi(app)


This example can then be run through an ASGI server, like `uvicorn
<https://www.uvicorn.org/>`_.
