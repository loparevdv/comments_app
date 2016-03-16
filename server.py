# import aiohttp.server
import aiopg
import asyncio
import aiopg

from aiohttp import web
from urllib.parse import urlparse, parse_qsl

# TODO:
# Define URLS, Comment.API, etc...
# Tests!
# ...

DB_ARGS = {
    'database': 'comment_app',
    'user': 'postgres',
    'password': 'postgres',
    'host': '127.0.0.1'
}


class Comment(object):

    @classmethod
    async def get_all(cls):
        connection = await aiopg.connect(**DB_ARGS)
        cursor = await connection.cursor()

        await cursor.execute("SELECT * FROM comment")
        return await cursor.fetchall()

    @classmethod
    async def get(cls, comment_id):
        connection = await aiopg.connect(**DB_ARGS)
        cursor = await connection.cursor()

        await cursor.execute("SELECT * FROM comment WHERE id=%s" % comment_id)
        return await cursor.fetchall()

    @classmethod
    async def get_thread(cls, root_id):
        connection = await aiopg.connect(**DB_ARGS)
        cursor = await connection.cursor()

        query = 'SELECT id, parent_id, comment_text, created, modified \
                 FROM comments_relations JOIN comment \
                 ON comments_relations.ancestor_id = comment.id \
                 WHERE ancestor_id= %s'

        await cursor.execute(query % root_id)
        return await cursor.fetchall()

    def create(cls):
        pass

    def update(cls):
        pass

    def delete(cls):
        pass


async def index(request):
    res = await Comment.get_all()
    data = str(res).encode('utf-8')
    return web.Response(body=data)

async def comment(request):
    comment_id = request.match_info['comment_id']
    res = await Comment.get(comment_id)
    data = str(res).encode('utf-8')
    return web.Response(body=data)

async def branch(request):
    root_id = request.match_info['root_id']
    res = await Comment.get_thread(root_id)
    data = str(res).encode('utf-8')
    return web.Response(body=data)


app = web.Application()
app.router.add_route('GET', '/', index)
app.router.add_route('GET', '/{comment_id}/', comment)
app.router.add_route('GET', '/branch/{root_id}/', branch)

web.run_app(app)
