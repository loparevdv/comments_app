from aiohttp import web

from models import Comment


async def get_one(request):
    comment_id = request.match_info['comment_id']
    res = await Comment.get(request, comment_id)
    return web.Response(body=str(res).encode('utf-8'))

async def create(request):
    post = await request.post()
    res = await Comment.create(request, post['user_id'], post['parent_id'], post['comment_text'])
    return web.Response()

async def update(request):
    comment_id = request.match_info['comment_id']
    post = await request.post()
    res = await Comment.update(request, comment_id, post['comment_text'])
    return web.Response(body=str(res).encode('utf-8'))

async def delete(request):
    comment_id = request.match_info['comment_id']
    res = await Comment.get_descendants_count(request, comment_id)
    desc_count = res[0] - 1
    # REQ - only comments without descendants can be deleted
    if desc_count == 0:
        await Comment.delete(request, comment_id)

    return web.Response(body=str(desc_count).encode('utf-8'))

async def branch(request):
    root_id = request.match_info['root_id']
    res = await Comment.get_thread(request, root_id)
    return web.Response(body=str(res).encode('utf-8'))

async def ent_branch(request):
    root_id = request.match_info['root_id']
    root_ct_id = request.match_info['root_content_type']
    res = await Comment.get_entity_thread(request, root_ct_id, root_id)
    return web.Response(body=str(res).encode('utf-8'))

async def ent_comments(request):
    root_id = request.match_info['root_id']
    root_ct_id = request.match_info['root_content_type']
    page = request.match_info['page']
    res = await Comment.get_entity_comments(request, root_ct_id, root_id, page)
    return web.Response(body=str(res).encode('utf-8'))

async def by_user(request):
    user_id = request.match_info['user_id']
    res = await Comment.get_user_comments(request, user_id)
    return web.Response(body=str(res).encode('utf-8'))
