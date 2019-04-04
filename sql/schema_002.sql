/*
DROP TABLE IF EXISTS data
DROP TABLE IF EXISTS webpage
DROP TABLE IF EXISTS users
*/
CREATE LANGUAGE plpythonu;


CREATE TABLE "webpage" (
	"id" serial UNIQUE,
	"url" VARCHAR(255),
	"model" VARCHAR(255) NOT NULL,
	"user_id" INTEGER NOT NULL,
	CONSTRAINT webpage_pk PRIMARY KEY ("url", "user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "users" (
	"id" serial UNIQUE,
	"name" VARCHAR(255),
	CONSTRAINT users_pk PRIMARY KEY ("name")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "data" (
	"id" serial NOT NULL,
	"webpage_id" INTEGER NOT NULL,
	"x" FLOAT NOT NULL,
	"y" FLOAT NOT NULL,
	"w" FLOAT NOT NULL,
	"h" FLOAT NOT NULL,
	"is_click" BOOLEAN NOT NULL,
	"ts" TIMESTAMP NOT NULL,
	CONSTRAINT data_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "webpage" ADD CONSTRAINT "webpage_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");


ALTER TABLE "data" ADD CONSTRAINT "data_fk0" FOREIGN KEY ("webpage_id") REFERENCES "webpage"("id");
