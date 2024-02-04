-- Prepares account information table
USE EZY;
CREATE TABLE IF NOT EXISTS account_information (
	user_id VARCHAR(100),
	login_time JSON,
	logout_time JSON,
	PRIMARY KEY (user_id)
);
