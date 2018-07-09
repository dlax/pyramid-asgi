from asgiref.testing import ApplicationCommunicator
from asgiref.wsgi import WsgiToAsgiInstance
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid import testing
import pytest
import webtest

from pyramid_asgi import PyramidWsgiToAsgi


def test_config():
    with testing.testConfig() as config:
        config.include('pyramid_asgi')
    assert 'protocol-router' in config.registry


class _TestConsumer(WsgiToAsgiInstance):

    async def __call__(self, receive, send):
        message = await receive()
        if message["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})


@pytest.mark.asyncio
async def test_protocol_router():

    def hello_view(request):
        return Response('Hello!')

    with Configurator() as config:
        config.include('pyramid_asgi')
        config.registry['protocol-router']['websocket']['/ws'] = _TestConsumer
        config.add_route('hello', '/hello')
        config.add_view(hello_view, route_name='hello')
        app = config.make_wsgi_app()
    asgi_app = PyramidWsgiToAsgi(app)

    # Websocket "type".
    instance = ApplicationCommunicator(asgi_app, {
        "type": "websocket",
        "path": "/ws",
    })
    await instance.send_input({"type": "websocket.connect"})
    output = await instance.receive_output(1)
    assert output == {'type': 'websocket.accept'}

    testapp = webtest.TestApp(app)
    res = testapp.get('/hello', status=200)
    assert 'Hello!' in res.text

    # HTTP type proxies to Pyramid route and view.
    instance = ApplicationCommunicator(asgi_app, {
        "type": "http",
        "http_version": "1.0",
        "method": "GET",
        "path": "/hello",
        "headers": [],
        "query_string": b"",
    })
    await instance.send_input({"type": "http.request"})
    output = await instance.receive_output(1)
    assert output['type'] == 'http.response.start'
    assert output['status'] == 200
    output = await instance.receive_output(1)
    assert output['type'] == 'http.response.body'
    assert output['body'] == b'Hello!'
    assert (await instance.receive_output(1)) == {
        'type': 'http.response.body',
    }
