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
	"type" INTEGER NOT NULL,
	"positionX" FLOAT,
	"positionY" FLOAT,
	"currentWidth" FLOAT,
	"currentHeight" FLOAT,
	"minutes" INTEGER,
	"seconds" INTEGER,
	"miliseconds" INTEGER,
	"keypress" INTEGER,
	"scrollPositionY" FLOAT,
	"scrollPositionX" FLOAT,
	"selectedText" INTEGER,
	"shiftPress" INTEGER,
	"ctrlPress" INTEGER,
	CONSTRAINT data_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "webpage" ADD CONSTRAINT "webpage_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");


ALTER TABLE "data" ADD CONSTRAINT "data_fk0" FOREIGN KEY ("webpage_id") REFERENCES "webpage"("id");


CREATE OR REPLACE FUNCTION model_change(webpage_id INTEGER, k INTEGER) RETURNS VOID AS 
$$import subprocess
subprocess.call(['/usr/bin/python', '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis.py', str(webpage_id), str(k)])
$$ LANGUAGE plpythonu;


DROP TRIGGER IF EXISTS insert_lim ON data

CREATE OR REPLACE FUNCTION trigg_befor_ins() RETURNS trigger AS ' -- для триггера
BEGIN 
if(select count(*) FROM data WHERE webpage_id = NEW.webpage_id) >= (select num_for_one_frame())
	then select model_change(NEW.webpage_id, select num_for_one_frame()); -- вызываем analysis.py
end if;
return NEW; -- делаем insert
END; 
' LANGUAGE  plpgsql;

CREATE TRIGGER insert_lim
BEFORE INSERT ON data
FOR EACH ROW 
EXECUTE PROCEDURE trigg_befor_ins(num_for_one_frame)

DELETE FROM data
DELETE FROM webpage
DELETE FROM users

COPY data TO '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/son.csv' DELIMITER ',' CSV HEADER;
