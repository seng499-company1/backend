CREATE DATABASE scheduler;
USE scheduler;

CREATE TABLE Admin (
	id BINARY(16) PRIMARY KEY,
	first_name VARCHAR(30),
	last_name VARCHAR(30),
	email VARCHAR(60) NOT NULL
);

CREATE TABLE Professor (
	id BINARY(16) PRIMARY KEY,
	first_name VARCHAR(30),
	last_name VARCHAR(30),
	email VARCHAR(60) NOT NULL,
	department VARCHAR(30) NOT NULL,
	is_teaching BOOLEAN NOT NULL
);

CREATE TABLE Schedule (
	id BINARY(16) PRIMARY KEY,
	schedule TEXT(50000) NOT NULL,
	semester CHAR NOT NULL,
	year int NOT NULL
);

CREATE TABLE CourseOffering (
	id BINARY(16) PRIMARY KEY,
	course_name VARCHAR(30) NOT NULL,
	course_code VARCHAR(10) NOT NULL, 
	min_offering INT NOT NULL,
	spring_required BOOLEAN NOT NULL,
	summer_required BOOLEAN NOT NULL,
	fall_required BOOLEAN NOT NULL,
	spring_peng_req BOOLEAN NOT NULL,
	summer_peng_req BOOLEAN NOT NULL,
	fall_peng_req BOOLEAN NOT NULL
);

CREATE TABLE ProfessorRelief (
	id  BINARY(16) PRIMARY KEY,
	prof_id  BINARY(16) NOT NULL,
	year INT NOT NULL,
	num_relief INT NOT NULL,
	num_summer_courses INT NOT NULL,
	num_fall_courses INT NOT NULL,
	num_spring_courses INT NOT NULL,
	FOREIGN KEY(prof_id)
		REFERENCES Professor(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE ProfessorCoursePreference (
	course_id BINARY(16) NOT NULL,
	prof_relief_id BINARY(16) NOT NULL,
	year INT NOT NULL,
	will_to_teach VARCHAR(12) NOT NULL,
	able_to_teach BOOLEAN NOT NULL,
	time_stamp DATETIME NOT NULL,
	FOREIGN KEY(prof_relief_id)
		REFERENCES ProfessorRelief(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY(course_id) 
		REFERENCES CourseOffering(id)
		On DELETE CASCADE
		ON UPDATE CASCADE,
	PRIMARY KEY(course_id, prof_relief_id)
);
