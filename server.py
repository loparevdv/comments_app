from aiohttp import web

import middlewares
from views import APIHandler

handler = APIHandler()
# so server...
app = web.Application(middlewares=[middlewares.middleware_factory])

# and urls...
app.router.add_route('GET', '/{comment_id}/', handler.get_one)
app.router.add_route('POST', '/create/', handler.create)
app.router.add_route('POST', '/update/{comment_id}/', handler.update)
app.router.add_route('DELETE', '/delete/{comment_id}/', handler.delete)
# TODO: rename to thread?
app.router.add_route('GET', '/branch/{root_id}/', handler.branch)
app.router.add_route('GET', '/ent_comments/{root_content_type}/{root_id}/page/{page}/', handler.ent_comments)
app.router.add_route('GET', '/ent_branch/{root_content_type}/{root_id}/', handler.ent_branch)
app.router.add_route('GET', '/user/{user_id}/', handler.by_user)
# NB: http://localhost:8080/report/1/2016-03-18T00:01:00+00:00/2016-03-18T16:17:57+00:00/
app.router.add_route('GET', '/report/{user_id}/{dt_start}/{dt_end}/', handler.get_report_by_user)
app.router.add_route('GET', '/report/{user_id}/', handler.get_report_by_user)

# uncomment to run without gunicorn
# web.run_app(app)
