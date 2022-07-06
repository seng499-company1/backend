USE scheduler;

LOAD DATA INFILE '/init_data/profs.txt' 
	INTO TABLE Professor
	FIELDS TERMINATED BY '\t'
	IGNORE 1 LINES
	(first_name,last_name,email,department,is_teaching,is_peng)
	SET id = UUID_TO_BIN(UUID());

LOAD DATA INFILE '/init_data/courses.txt' 
	INTO TABLE CourseOffering
	FIELDS TERMINATED BY '\t'
	IGNORE 1 LINES
	(course_name,course_code,course_desc,prof_prereq,min_offering,spring_req,summer_req,fall_req,spring_peng_req,summer_peng_req,fall_peng_req,year_req,notes)
	SET id = UUID_TO_BIN(UUID());
