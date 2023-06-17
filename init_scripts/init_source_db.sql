CREATE TABLE IF NOT EXISTS "movies" (
  "id" uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  "title" VARCHAR(255) NOT NULL,
  "description" TEXT,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "movies_id-idx" ON "movies"("id");
CREATE INDEX "movies_updated_at-idx" ON "movies"("updated_at");


CREATE OR REPLACE  FUNCTION update_updated_at_movie() RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
    BEGIN
        SET TIMEZONE TO 'Europe/Moscow';
        NEW.updated_at = now();
        RETURN NEW;
    END;
$$;

CREATE TRIGGER update_user_task_updated_on
    BEFORE UPDATE
    ON
        public.movies
    FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_movie();

