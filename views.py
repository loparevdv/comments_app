from aiohttp import web

from models import Comment

#TODO: maybe instantiatable class should be implemented to provide and manage database connection

async def get_one(request):
    comment_id = request.match_info['comment_id']
    res = await Comment.get(request, comment_id)
    return web.Response(body=str(res).encode('utf-8'))

async def create(request):
    post = await request.post()

    main_args = post.get('user_id'), post.get('parent_id'), post.get('comment_text')
    assert all(main_args)

    additionam_args = post.get('root_content_type'), post.get('root_id')
    kwargs = {}
    if all(additionam_args):
        kwargs = {
            'root_content_type': additionam_args[0],
            'root_id': additionam_args[1],
        }

    res = await Comment.create(request, *main_args, **kwargs)
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

    return web.Response()

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

async def get_report_by_user(request):
    user_id = request.match_info['user_id']

    kwargs = {
        'dt_start': request.match_info.get('dt_start'),
        'dt_end': request.match_info.get('dt_end'),
    }
    res = await Comment.get_user_comments(request, user_id, **kwargs)

    # TODO: better replace with streaming response or something
    xml_start = '<?xml version="1.0" encoding="utf-8"?><comments>'
    comment_xml_row = '<Comment><id>%s</id><parent_id>%s</parent_id><user_id>%s</user_id><text>"%s"</text></Comment>'
    for row in res:
        xml_start += comment_xml_row % (row[0], row[1], row[2], row[3])
    xml_start += '</comments>'

    return web.Response(content_type='xml', body=str(xml_start).encode('utf-8'))
