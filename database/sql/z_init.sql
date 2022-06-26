USE scheduler;

-- https://dev.mysql.com/doc/refman/8.0/en/load-data.html
LOAD DATA INFILE '/csv/profs.csv' 
	INTO TABLE Professor
	FIELDS TERMINATED BY ','
	IGNORE 1 LINES
	(first_name,last_name,email,department,is_teaching,is_peng)
	SET id = UUID_TO_BIN(UUID());
