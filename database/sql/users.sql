CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE, DELETE ON scheduler.* TO 'api_user'@localhost;
FLUSH PRIVILEGES;
