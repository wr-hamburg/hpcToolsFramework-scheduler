CREATE TABLE IF NOT EXISTS "programs" (
    "id" serial,
    "name" text,
    "makefile_path" text,
    "program_path" text,
    "directory" text,
    PRIMARY KEY( id )
);

CREATE TABLE IF NOT EXISTS "jobs" (
    "id" serial,
    "timestamp_id" text,
    "makefile_path" text,
    "jobscript_path" text,
    "status" text,
    "program_id" integer,
    "queue_time" timestamp,
    "start_time" timestamp,
    "finish_time" timestamp,
    PRIMARY KEY( id ),
FOREIGN KEY (program_id) REFERENCES programs (id)

);
