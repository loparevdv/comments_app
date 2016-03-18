import asyncio

from aiohttp import web
from middlewares import middleware_factory

import views

# TODO: wow so much. split on two files views - server
app = web.Application(middlewares=[middleware_factory])
app.router.add_route('GET', '/{comment_id}/', views.get_one)
app.router.add_route('POST', '/create/', views.create)
app.router.add_route('POST', '/update/{comment_id}/', views.update)
app.router.add_route('DELETE', '/delete/{comment_id}/', views.delete)
# TODO: rename to thread?
app.router.add_route('GET', '/branch/{root_id}/', views.branch)
app.router.add_route('GET', '/ent_comments/{root_content_type}/{root_id}/page/{page}/', views.ent_comments)
app.router.add_route('GET', '/ent_branch/{root_content_type}/{root_id}/', views.ent_branch)
app.router.add_route('GET', '/user/{user_id}/', views.by_user)

# web.run_app(app)
