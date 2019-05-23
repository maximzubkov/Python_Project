/*
DROP TABLE IF EXISTS data
DROP TABLE IF EXISTS hmm
DROP TABLE IF EXISTS webpage
DROP TABLE IF EXISTS users
*/
CREATE LANGUAGE plpythonu;


CREATE TABLE "webpage" (
	"id" INTEGER NOT NULL UNIQUE,
	"url" VARCHAR(255),
	"model" VARCHAR(255) NOT NULL,
	"user_id" INTEGER NOT NULL,
	"time_on_page" FLOAT,
	CONSTRAINT webpage_pk PRIMARY KEY ("url", "user_id")
) WITH (
  OIDS=FALSE
);


CREATE TABLE "users" (
	"id" serial UNIQUE,
	"name" VARCHAR(255) NOT NULL,
	"password" VARCHAR(255) NOT NULL,
	"status" INTEGER NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY ("name")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "hmm" (
	"transition" FLOAT [][],
	"emission" FLOAT [][],
	"distribution" FLOAT [],
	"status" INTEGER,
	"user_id" INTEGER,
	CONSTRAINT transition_pk PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);


ALTER TABLE "webpage" ADD CONSTRAINT "webpage_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");

ALTER TABLE "hmm" ADD CONSTRAINT "hmm_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");

COPY data TO '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/son.csv' DELIMITER ',' CSV HEADER;

