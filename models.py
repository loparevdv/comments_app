# WOW NO IMPORTS

class Comment(object):

    @classmethod
    async def get(cls, request, comment_id):
        query = 'SELECT * FROM comment WHERE id = %s'
        cur = await request.pool.cursor()
        await cur.execute(query, (comment_id, ))
        return await cur.fetchall()

    @classmethod
    async def create(cls, request, parent_id, text):
        if int(parent_id):
            query = 'INSERT INTO comment (parent_id, comment_text) VALUES (%s, %s)'
            args = (parent_id, text)
        else:
            query = 'INSERT INTO comment (comment_text) VALUES (%s)'
            args = (text, )
        
        cur = await request.pool.cursor()
        return await cur.execute(query, args)

    @classmethod
    async def update(cls, request, comment_id, comment_text):
        cur = await request.pool.cursor()
        query = 'UPDATE comment SET comment_text = %s WHERE id = %d;'
        args = (comment_text, int(comment_id))
        return await cur.execute(query, args)

    @classmethod
    async def delete(cls, request, comment_id):
        await cls._flush_relations(request, comment_id)
        cur = await request.pool.cursor()
        query = 'DELETE FROM comment WHERE id = %d'
        return await cur.execute(query, (int(comment_id), ))

    @classmethod
    async def _flush_relations(cls, request, comment_id):
        cur = await request.pool.cursor()
        query = 'DELETE FROM comments_relations WHERE ancestor_id = %d OR descendant_id = %d'
        await cur.execute(query, (int(comment_id), int(comment_id), ))
        return await cur.fetchone()

    @classmethod
    async def get_descendants_count(cls, request, comment_id):
        cur = await request.pool.cursor()
        query = 'SELECT count(*) FROM comments_relations WHERE ancestor_id = %d;'
        await cur.execute(query, (int(comment_id), ))
        return await cur.fetchone()

    @classmethod
    async def get_thread(cls, request, root_id):
        query = 'SELECT id, parent_id, comment_text, created, modified \
                 FROM comments_relations JOIN comment \
                 ON comments_relations.descendant_id = comment.id \
                 WHERE ancestor_id= %s'

        cur = await request.pool.cursor()
        await cur.execute(query, (root_id, ))
        return await cur.fetchall()

    @classmethod
    async def get_entity_thread(cls, request, root_content_type, root_id):
        query = 'SELECT id, parent_id, comment_text, created, modified \
        FROM comments_relations JOIN comment \
        ON comments_relations.descendant_id = comment.id \
        WHERE ancestor_id IN (SELECT id from comment where root_content_type = %s and root_id = %s);'

        cur = await request.pool.cursor()
        await cur.execute(query, (root_content_type, root_id))
        return await cur.fetchall()
