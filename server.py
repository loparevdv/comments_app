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

        await cursor.execute('SELECT * FROM comment WHERE id=%s' % comment_id)
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

    @classmethod
    async def create(cls, parent_id, text):
        connection = await aiopg.connect(**DB_ARGS)
        cursor = await connection.cursor()

        if int(parent_id):
            query = 'INSERT INTO comment (parent_id, comment_text) VALUES (%s, %s)'
            args = (parent_id, text)
        else:
            query = 'INSERT INTO comment (comment_text) VALUES (%s)'
            args = (text, )

        return await cursor.execute(query % args)

    def update(cls):
        pass

    def delete(cls):
        pass

    @classmethod
    async def get_descendants_count(cls):
        connection = await aiopg.connect(**DB_ARGS)
        cursor = await connection.cursor()


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

async def create(request):
    post = await request.post()
    res = await Comment.create(post['parent_id'], post['comment_text'])
    data = str(res).encode('utf-8')
    return web.Response(body=data)

async def update(request):
    root_id = request.match_info['root_id']

async def delete(request):
    # REQ - only comments without descendants can be deleted
    root_id = request.match_info['root_id']


app = web.Application()
app.router.add_route('GET', '/', index)
app.router.add_route('GET', '/{comment_id}/', comment)
app.router.add_route('POST', '/create/', create)
app.router.add_route('POST', '/update/{comment_id}/', update)
app.router.add_route('DELETE', '/delete/{comment_id}/', comment)

app.router.add_route('GET', '/branch/{root_id}/', branch)

web.run_app(app)
