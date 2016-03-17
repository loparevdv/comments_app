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
    async def get(cls, request, comment_id):
        query = 'SELECT * FROM comment WHERE id=%s'

        with (request.cursor) as cur:
            await cur.execute(query % (comment_id, ))
            return await cur.fetchall()

    @classmethod
    async def get_thread(cls, request, root_id):

        query = 'SELECT id, parent_id, comment_text, created, modified \
                 FROM comments_relations JOIN comment \
                 ON comments_relations.descendant_id = comment.id \
                 WHERE ancestor_id= %s'

        with (request.cursor) as cur:
            await cur.execute(query % (root_id, ))
            return await cur.fetchall()

    @classmethod
    async def create(cls, request, parent_id, text):

        if int(parent_id):
            query = 'INSERT INTO comment (parent_id, comment_text) VALUES (%s, %s)'
            args = (parent_id, text)
        else:
            query = 'INSERT INTO comment (comment_text) VALUES (%s)'
            args = (text, )
        
        with (request.cursor) as cur:
            return await cur.execute(query % args)

    @classmethod
    async def update(cls, request, comment_id, comment_text):
        query = 'update comment set comment_text = %s where id = %d;'
        args = (comment_text, int(comment_id))

        with (request.cursor) as cur:
            return await cur.execute(query % args)

    def delete(cls):
        pass

    @classmethod
    async def get_descendants_count(cls):
        connection = await aiopg.connect(**DB_ARGS)
        cursor = await connection.cursor()


async def comment(request):
    comment_id = request.match_info['comment_id']
    res = await Comment.get(comment_id)
    data = str(res).encode('utf-8')
    return web.Response(body=data)

async def branch(request):
    root_id = request.match_info['root_id']
    res = await Comment.get_thread(request, root_id)
    data = str(res).encode('utf-8')
    return web.Response(body=data)

async def create(request):
    post = await request.post()
    res = await Comment.create(request, post['parent_id'], post['comment_text'])
    data = str(res).encode('utf-8')
    return web.Response(body=data)

async def update(request):
    comment_id = request.match_info['comment_id']
    post = await request.post()
    res = await Comment.update(request, comment_id, post['comment_text'])
    data = str(res).encode('utf-8')
    return web.Response(body=data)

async def delete(request):
    # REQ - only comments without descendants can be deleted
    root_id = request.match_info['root_id']


async def middleware_factory(app, handler):

    async def middleware_handler(request):
        dsn = 'dbname=comment_app user=postgres password=postgres host=localhost port=5432'
        pool = await aiopg.create_pool(dsn)
        cursor = await pool.cursor()
        request.cursor = cursor
        return await handler(request)

    return middleware_handler


app = web.Application(middlewares=[middleware_factory])

app.router.add_route('GET', '/{comment_id}/', comment)
app.router.add_route('POST', '/create/', create)
app.router.add_route('POST', '/update/{comment_id}/', update)
app.router.add_route('DELETE', '/delete/{comment_id}/', comment)

app.router.add_route('GET', '/branch/{root_id}/', branch)

web.run_app(app)
