/*
Что в одних коментах "--" нужно раскоментить и по идее должно получиться
Что в двойных "-- --" просто комментарии
Исправить язык: "LANGUAGE plpgsql" убрать в одном месте
*/


CREATE OR REPLACE FUNCTION num_for_one_frame() RETURNS int LANGUAGE plpgsql AS $$ -- создание переменной
DECLARE
  num_for_one_frame int;
BEGIN
  num_for_one_frame := 5;
  RETURN num_for_one_frame;
END
$$;

-- CREATE LANGUAGE plpythonu; -- create language if does not exist
-- -- DROP FUNCTION model_change(integer,integer)

CREATE OR REPLACE FUNCTION model_change(webpage_id INTEGER,inout k INTEGER) RETURNS INT LANGUAGE plpgsql AS -- исправить язык "LANGUAGE plpgsql" убрать 
  $$
-- BEGIN
-- 	INSERT INTO users VALUES(9,'ShF');
 	import subprocess
 	subprocess.call(['/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis.py, str(webpage_id), str(k)'])
-- -- 	RETURN k;
-- END
  $$;
-- LANGUAGE plpythonu;

-- -- select model_change(3, 10)

DROP TRIGGER IF EXISTS insert_lim ON data

CREATE OR REPLACE FUNCTION trigg_after_ins() RETURNS trigger AS ' -- для триггера
DECLARE
	k INT;
	t INT;
BEGIN 
	k := num_for_one_frame();
	if((select count(*) FROM data WHERE webpage_id = NEW.webpage_id) % k = 0)
		then t = model_change(NEW.webpage_id, 10); -- вызываем analysis.py
	end if;
	return NEW;
END; 
' LANGUAGE  plpgsql;

CREATE TRIGGER insert_lim
AFTER INSERT ON data
FOR EACH ROW 
EXECUTE PROCEDURE trigg_after_ins()
