DROP TABLE IF EXISTS comments_relations;
DROP TABLE IF EXISTS comment;

CREATE TABLE comment(
   id integer,
   parent_id integer REFERENCES comment,
   comment_text varchar(255),

   created timestamp,
   modified timestamp DEFAULT current_timestamp,

   root_id integer,
   root_content_type integer,
   PRIMARY KEY (id)
);

CREATE TABLE comments_relations(
   ancestor_id integer NOT NULL REFERENCES comment,
   descendant_id integer NOT NULL REFERENCES comment,
   PRIMARY KEY (ancestor_id, descendant_id)
)
