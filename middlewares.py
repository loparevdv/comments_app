import aiopg

# TODO: make dsn from this dict, move dict to settings.py
DB_ARGS = {
    'database': 'comment_app',
    'user': 'postgres',
    'password': 'postgres',
    'host': '127.0.0.1'
}

async def middleware_factory(app, handler):

    async def middleware_handler(request):
        dsn = 'dbname=comment_app user=postgres password=postgres host=localhost port=5432'
        pool = await aiopg.create_pool(dsn=dsn, minsize=5, maxsize=5)
        request.pool = await pool.acquire()
        return await handler(request)

    return middleware_handler
