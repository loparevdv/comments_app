import asyncio

from aiohttp import web
from urllib.parse import urlparse, parse_qsl
from middlewares import middleware_factory
from models import Comment


async def comment(request):
    comment_id = request.match_info['comment_id']
    res = await Comment.get(request, comment_id)
    return web.Response(body=str(res).encode('utf-8'))

async def branch(request):
    root_id = request.match_info['root_id']
    res = await Comment.get_thread(request, root_id)
    return web.Response(body=str(res).encode('utf-8'))

async def create(request):
    post = await request.post()
    res = await Comment.create(request, post['parent_id'], post['comment_text'])
    return web.Response(body=str(res).encode('utf-8'))

async def update(request):
    comment_id = request.match_info['comment_id']
    post = await request.post()
    res = await Comment.update(request, comment_id, post['comment_text'])
    return web.Response(body=str(res).encode('utf-8'))

async def delete(request):
    comment_id = request.match_info['comment_id']
    res = await Comment.get_descendants_count(request, comment_id)

    desc_count = res[0] - 1
    # desc_count = 0
    # REQ - only comments without descendants can be deleted
    if desc_count == 0:
        await Comment.delete(request, comment_id)

    return web.Response(body=str(desc_count).encode('utf-8'))

app = web.Application(middlewares=[middleware_factory])

app.router.add_route('GET', '/{comment_id}/', comment)
app.router.add_route('POST', '/create/', create)
app.router.add_route('POST', '/update/{comment_id}/', update)
app.router.add_route('DELETE', '/delete/{comment_id}/', delete)

app.router.add_route('GET', '/branch/{root_id}/', branch)

web.run_app(app)
