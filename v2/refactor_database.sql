-- refactors the ezy database as of 27-12-2023

CREATE DATABASE `EZY`;
CREATE TABLE EZY.google_users LIKE Ezy_url.users;
INSERT INTO EZY.google_users
SELECT * FROM Ezy_url.users;

-- now databse EZY has the google_users as the users table
-- now create ezy_users table in EZY database

CREATE TABLE EZY.ezy_users LIKE EZY.google_users;
INSERT INTO EZY.ezy_users
SELECT * FROM EZY.google_users WHERE google_id LIKE 'N/A';

-- Now drop unwanted colum on each table and users from google_table

ALTER TABLE EZY.google_users
DROP COLUMN password,
DROP COLUMN authentication_method;

ALTER TABLE EZY.ezy_users
DROP COLUMN authentication_method,
DROP COLUMN google_id;

DELETE FROM EZY.google_users WHERE google_id = 'N/A';

-- change some column names like Two_factor to two_factor in both users table

ALTER TABLE EZY.google_users
CHANGE Two_factor two_factor VARCHAR(50),
CHANGE Two_factor_status two_factor_status VARCHAR(15);

ALTER TABLE EZY.ezy_users
CHANGE Two_factor two_factor VARCHAR(50),
CHANGE Two_factor_status two_factor_status VARCHAR(15);

-- Now add column profile_pic

ALTER TABLE EZY.google_users
ADD COLUMN profile_pic VARCHAR(100) DEFAULT 'N/A' NOT NULL;

ALTER TABLE EZY.ezy_users
ADD COLUMN profile_pic VARCHAR(5) DEFAULT 'N/A' NOT NULL;
