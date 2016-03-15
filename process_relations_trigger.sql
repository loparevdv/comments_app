DROP TRIGGER IF EXISTS process_relations on comment;
DROP FUNCTION IF EXISTS process_relations();

CREATE FUNCTION process_relations() RETURNS trigger AS $process_relations$
    BEGIN

        INSERT INTO comments_relations(ancestor_id, descendant_id)
        SELECT ancestor_id, NEW.id
        FROM comments_relations
        WHERE descendant_id = NEW.parent_id
        UNION ALL SELECT NEW.id, NEW,id;

        RETURN NEW;
    END;
$process_relations$ LANGUAGE plpgsql;

CREATE TRIGGER process_relations AFTER INSERT ON comment
    FOR EACH ROW EXECUTE PROCEDURE process_relations();