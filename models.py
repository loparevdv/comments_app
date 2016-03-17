# WOW NO IMPORTS

class Comment(object):

    @classmethod
    async def get(cls, request, comment_id):
        query = 'SELECT * FROM comment WHERE id = %s'

        async with (request.pool.cursor()) as cur:
            await cur.execute(query % (comment_id, ))
            return await cur.fetchall()

    @classmethod
    async def get_thread(cls, request, root_id):

        query = 'SELECT id, parent_id, comment_text, created, modified \
                 FROM comments_relations JOIN comment \
                 ON comments_relations.descendant_id = comment.id \
                 WHERE ancestor_id= %s'

        async with (request.pool.cursor()) as cur:
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
        
        async with (request.pool.cursor()) as cur:
            return await cur.execute(query % args)

    @classmethod
    async def update(cls, request, comment_id, comment_text):
        async with (request.pool.cursor()) as cur:
            query = 'UPDATE comment SET comment_text = %s WHERE id = %d;'
            args = (comment_text, int(comment_id))
            return await cur.execute(query % args)

    @classmethod
    async def get_descendants_count(cls, request, comment_id):
        async with (request.pool.cursor()) as cur:
            query = 'SELECT count(*) FROM comments_relations WHERE ancestor_id = %d;'
            await cur.execute(query % (int(comment_id), ))
            res = await cur.fetchone()
            return res

    @classmethod
    async def _flush_relations(cls, request, comment_id):
        async with (request.pool.cursor()) as cur:
            query = 'DELETE FROM comments_relations WHERE ancestor_id = %d OR descendant_id = %d'
            await cur.execute(query % (int(comment_id), int(comment_id), ))
            res = cur.fetchone()
            return res

    @classmethod
    async def delete(cls, request, comment_id):
        await cls._flush_relations(request, comment_id)

        async with (request.pool.cursor()) as cur:
            query = 'DELETE FROM comment WHERE id = %d'
            return await cur.execute(query % (int(comment_id), ))
