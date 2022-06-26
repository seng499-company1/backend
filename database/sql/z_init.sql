USE scheduler;

-- https://dev.mysql.com/doc/refman/8.0/en/load-data.html
LOAD DATA INFILE '/csv/profs.csv' 
	INTO TABLE Professor
	FIELDS TERMINATED BY ','
	IGNORE 1 LINES
	(first_name,last_name,email,department,is_teaching,is_peng)
	SET id = UUID_TO_BIN(UUID());

LOAD DATA INFILE '/csv/courses.csv' 
	INTO TABLE CourseOffering
	FIELDS TERMINATED BY ','
	IGNORE 1 LINES
	(course_name,course_code,course_desc,prof_prereq,min_offering,spring_req,summer_req,fall_req,spring_peng_req,summer_peng_req,fall_peng_req)
	SET id = UUID_TO_BIN(UUID());
