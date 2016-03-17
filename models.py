# WOW NO IMPORTS

class Comment(object):

    @classmethod
    async def get(cls, request, comment_id):
        query = 'SELECT * FROM comment WHERE id=%s'

        with (request.cursor) as cur:
            await cur.execute(query % (comment_id, ))
            return await cur.fetchall()

    @classmethod
    async def get_thread(cls, request, root_id):

        query = 'SELECT id, parent_id, comment_text, created, modified \
                 FROM comments_relations JOIN comment \
                 ON comments_relations.descendant_id = comment.id \
                 WHERE ancestor_id= %s'

        with (request.cursor) as cur:
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
        
        with (request.cursor) as cur:
            return await cur.execute(query % args)

    @classmethod
    async def update(cls, request, comment_id, comment_text):
        query = 'update comment set comment_text = %s where id = %d;'
        args = (comment_text, int(comment_id))

        with (request.cursor) as cur:
            return await cur.execute(query % args)

    def delete(cls):
        pass
