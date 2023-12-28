-- sql script to alter table users

USE Ezy_url;

ALTER TABLE users DROP COLUMN verified;
ALTER TABLE users ADD COLUMN verified VARCHAR(20) DEFAULT 'No';
ALTER TABLE users MODIFY COLUMN Two_factor VARCHAR(50) DEFAULT 'disabled';
ALTER TABLE users ADD COLUMN authentication_method VARCHAR(20) DEFAULT 'Ezy';
ALTER TABLE users MODIFY COLUMN password VARCHAR(255) DEFAULT NULL;
ALTER TABLE users ADD COLUMN google_id VARCHAR(200) DEFAULT 'N/A';
ALTER TABLE users ADD COLUMN Two_factor_status VARCHAR(15) DEFAULT 'disabled';
