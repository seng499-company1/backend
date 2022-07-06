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
	is_teaching BOOLEAN NOT NULL,
	is_peng BOOLEAN NOT NULL
);

CREATE TABLE Schedule (
	id BINARY(16) PRIMARY KEY,
	result JSON NOT NULL,
	semester CHAR NOT NULL,
	year int NOT NULL
);

CREATE TABLE Algo2Output (
	id BINARY(16) PRIMARY KEY,
	result JSON NOT NULL,
	semester CHAR NOT NULL,
	year int NOT NULL
);

CREATE TABLE HistoricalData(
	id BINARY(16) PRIMARY KEY,
	result JSON NOT NULL
);

CREATE TABLE CourseOffering (
	id BINARY(16) PRIMARY KEY,
	course_name VARCHAR(100) NOT NULL,
	course_code VARCHAR(10) NOT NULL, 
	course_desc VARCHAR(2000) NOT NULL,
	prof_prereq VARCHAR(500),
	min_offering INT NOT NULL,
	spring_req BOOLEAN NOT NULL,
	summer_req BOOLEAN NOT NULL,
	fall_req BOOLEAN NOT NULL,
	spring_peng_req BOOLEAN NOT NULL,
	summer_peng_req BOOLEAN NOT NULL,
	fall_peng_req BOOLEAN NOT NULL,
	year_req INT NOT NULL,
	notes VARCHAR(500)
);

CREATE TABLE ProfessorAvailability (
	id  BINARY(16) PRIMARY KEY,
	prof_id  BINARY(16) NOT NULL,
	year INT NOT NULL,
	num_relief INT NOT NULL,
	why_relief VARCHAR(100),
	num_summer_courses INT NOT NULL,
	num_fall_courses INT NOT NULL,
	num_spring_courses INT NOT NULL,
	preferred_times JSON,
	FOREIGN KEY(prof_id)
		REFERENCES Professor(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE ProfessorCoursePreference (
	course_id BINARY(16) NOT NULL,
	prof_avail_id BINARY(16) NOT NULL,
	year INT NOT NULL,
	will_to_teach VARCHAR(12) NOT NULL,
	able_to_teach VARCHAR(12) NOT NULL,
	time_stamp DATETIME default now(),
	FOREIGN KEY(prof_avail_id)
		REFERENCES ProfessorAvailability(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY(course_id) 
		REFERENCES CourseOffering(id)
		On DELETE CASCADE
		ON UPDATE CASCADE,
	PRIMARY KEY(course_id, prof_avail_id)
);
