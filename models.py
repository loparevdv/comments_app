# WOW NO IMPORTS


class Comment(object):
    # TODO: think about to make it insantiable to store cursor and autoclose connection
    # TODO: at least propagate connection closing for defence programming sake!

    @classmethod
    async def get(cls, request, comment_id):
        query = 'SELECT * FROM comment WHERE id = %s'
        cur = await request.pool.cursor()
        await cur.execute(query, (comment_id, ))
        return await cur.fetchall()

    @classmethod
    async def create(cls, request, user_id, parent_id, text, **kwargs):
        if int(parent_id):
            query = 'INSERT INTO comment (user_id, parent_id, comment_text) VALUES (%s, %s, %s)'
            args = (user_id, parent_id, text)
        else:
            query = 'INSERT INTO comment (user_id, comment_text) VALUES (%s, %s)'
            args = (user_id, text, )

        cur = await request.pool.cursor()
        res = await cur.execute(query, args)
        cur.connection.close()
        return res

    @classmethod
    async def update(cls, request, comment_id, comment_text):
        cur = await request.pool.cursor()
        query = 'UPDATE comment SET comment_text = %s WHERE id = %d;'
        args = (comment_text, int(comment_id))
        res = await cur.execute(query, args)
        cur.connection.close()
        return res

    @classmethod
    async def delete(cls, request, comment_id):
        await cls._flush_relations(request, comment_id)
        cur = await request.pool.cursor()
        query = 'DELETE FROM comment WHERE id = %d'
        return await cur.execute(query, (int(comment_id), ))

    @classmethod
    async def _flush_relations(cls, request, comment_id):
        # REQ - only connections without descendants can be deleted
        # but this query is more generic
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
        # getting whole thread in ONE QUERY.
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
        WHERE ancestor_id IN (SELECT id from comment where root_content_type=%s and root_id=%s);'

        cur = await request.pool.cursor()
        await cur.execute(query, (root_content_type, root_id))
        return await cur.fetchall()

    @classmethod
    async def get_entity_comments(cls, request, root_content_type, root_id, page):
        query = 'SELECT id, parent_id, comment_text, created, modified \
        FROM comment WHERE root_content_type = %s AND root_id = %s \
        LIMIT 10 OFFSET %s;'
        # TODO: make 10 setting constant
        cur = await request.pool.cursor()
        await cur.execute(query, (root_content_type, root_id, (int(page)-1)*10))
        return await cur.fetchall()

    @classmethod
    async def get_user_comments(cls, request, user_id, **kwargs):
        query = 'SELECT id, parent_id, user_id, comment_text, created, modified \
        FROM comment WHERE user_id = %s '

        dt_start = kwargs.get('dt_start')
        dt_end = kwargs.get('dt_end')
        args = [user_id]

        if dt_start:
            args.append(dt_start)
            query += ' AND modified > %s'

        if dt_end:
            args.append(dt_end)
            query += ' AND modified < %s'

        cur = await request.pool.cursor()
        return await cur.execute(query, args)
