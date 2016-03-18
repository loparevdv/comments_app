DROP TABLE IF EXISTS comments_relations;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS sysuser;

CREATE TABLE sysuser(
   id serial PRIMARY KEY,
   username varchar(64)
);
INSERT INTO sysuser (username) VALUES ('default');

CREATE TABLE comment(
   id serial PRIMARY KEY,
   user_id integer REFERENCES sysuser NOT NULL,
   parent_id integer REFERENCES comment DEFAULT NULL,
   comment_text varchar(255),

   created timestamp,
   modified timestamp DEFAULT current_timestamp,

   root_id integer,
   root_content_type integer
);

CREATE TABLE comments_relations(
   ancestor_id integer NOT NULL REFERENCES comment,
   descendant_id integer NOT NULL REFERENCES comment,
   PRIMARY KEY (ancestor_id, descendant_id)
);

DROP TRIGGER IF EXISTS process_relations on comment;
DROP FUNCTION IF EXISTS process_relations();

CREATE FUNCTION process_relations() RETURNS trigger AS $process_relations$
    BEGIN

        INSERT INTO comments_relations(ancestor_id, descendant_id)
        SELECT ancestor_id, NEW.id
        FROM comments_relations
        WHERE descendant_id = NEW.parent_id
        UNION ALL SELECT NEW.id, NEW.id;

        RETURN NEW;
    END;
$process_relations$ LANGUAGE plpgsql;

CREATE TRIGGER process_relations AFTER INSERT ON comment
    FOR EACH ROW EXECUTE PROCEDURE process_relations();

insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
insert into sysuser (username) values ('dafuq');
