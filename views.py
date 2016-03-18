from aiohttp import web

import xml_report
from models import Comment

# TODO: maybe instantiatable class should be implemented to provide and manage database connection

reporting_methods = {
    'xml': xml_report.get_xml,
}


class APIHandler:

    def __init__(self):
        pass

    async def get_one(self, request):
        comment_id = request.match_info['comment_id']
        res = await Comment.get(request, comment_id)
        return web.Response(body=str(res).encode('utf-8'))

    async def create(self, request):
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

    async def update(self, request):
        comment_id = request.match_info['comment_id']
        post = await request.post()
        res = await Comment.update(request, comment_id, post['comment_text'])
        return web.Response(body=str(res).encode('utf-8'))

    async def delete(self, request):
        comment_id = request.match_info['comment_id']
        res = await Comment.get_descendants_count(request, comment_id)
        desc_count = res[0] - 1
        # REQ - only comments without descendants can be deleted
        if desc_count == 0:
            await Comment.delete(request, comment_id)

        return web.Response()

    async def branch(self, request):
        root_id = request.match_info['root_id']
        res = await Comment.get_thread(request, root_id)
        return web.Response(body=str(res).encode('utf-8'))

    async def ent_branch(self, request):
        root_id = request.match_info['root_id']
        root_ct_id = request.match_info['root_content_type']
        res = await Comment.get_entity_thread(request, root_ct_id, root_id)
        return web.Response(body=str(res).encode('utf-8'))

    async def ent_comments(self, request):
        root_id = request.match_info['root_id']
        root_ct_id = request.match_info['root_content_type']
        page = request.match_info['page']
        res = await Comment.get_entity_comments(request, root_ct_id, root_id, page)
        return web.Response(body=str(res).encode('utf-8'))

    async def by_user(self, request):
        user_id = request.match_info['user_id']
        res = await Comment.get_user_comments(request, user_id)
        return web.Response(body=str(res).encode('utf-8'))

    async def get_report_by_user(self, request):
        # TODO: very naive.
        # TODO: got to be replaced with websocket and streaming xml generation/file reading
        REPORT_TYPE = 'xml'
        user_id = request.match_info['user_id']

        dt_start = request.match_info.get('dt_start')
        dt_end = request.match_info.get('dt_end')

        kwargs = {
            'dt_start': dt_start,
            'dt_end': dt_end,
        }

        report_filename = '%s_%s_%s.xml' % (user_id,
                                            dt_start.split('+')[0].replace(':', '_'),
                                            dt_end.split('+')[0].replace(':', '_'))
        try:
            f = open(report_filename, 'r')
        except FileNotFoundError:
            f = open(report_filename, 'w')

        is_found = f.mode == 'r'
        if not is_found:
            raw_comments = await Comment.get_user_comments(request, user_id, **kwargs)
            xml_response = reporting_methods[REPORT_TYPE](raw_comments)
            f.write(xml_response)
        else:
            xml_response = f.read()

        return web.Response(content_type=REPORT_TYPE, body=str(xml_response).encode('utf-8'))
