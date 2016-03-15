
from urllib.parse import urlparse, parse_qsl

import aiohttp
import aiohttp.server
import aiopg
from aiohttp import MultiDict

import asyncio
import aiopg

@asyncio.coroutine
def get_comments():
    conn = yield from aiopg.connect(database='comment_app',
                                    user='postgres',
                                    password='postgres',
                                    host='127.0.0.1')
    cur = yield from conn.cursor()
    yield from cur.execute("SELECT * FROM comment")
    ret = yield from cur.fetchall()
    return ret


class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):

    async def handle_request(self, message, payload):
        response = aiohttp.Response(
            self.writer, 200, http_version=message.version
        )
        res = await get_comments()
        data = str(res)
        response.add_header('Content-Type', 'text/html')
        response.add_header('Content-Length', str(len(data)))
        response.send_headers()
        response.write(data.encode('utf-8'))
        await response.write_eof()


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    f = loop.create_server(lambda: HttpRequestHandler(debug=True, keep_alive=75), '0.0.0.0', '8080')
    srv = loop.run_until_complete(f)

    print('serving on', srv.sockets[0].getsockname())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

