CREATE OR REPLACE FUNCTION notify_etl() RETURNS TRIGGER AS $$
BEGIN
PERFORM pg_notify('update_or_insert_event', 'Data has been updated or inserted in the table');
RETURN NULL;
END;
$$ LANGUAGE plpgsql;
