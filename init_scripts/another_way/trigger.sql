CREATE TRIGGER update_insert_trigger
AFTER INSERT OR UPDATE ON content.film_work
FOR EACH ROW
EXECUTE FUNCTION content.notify_etl();
