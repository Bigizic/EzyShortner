-- sql script to alter table users

USE Ezy_url;

ALTER TABLE users DROP COLUMN verified;
ALTER TABLE users ADD COLUMN verified VARCHAR(20) DEFAULT 'No';
ALTER TABLE users ADD COLUMN Two_factor VARCHAR(20) DEFAULT 'disabled';
ALTER TABLE users ADD COLUMN authentication_method VARCHAR(20) DEFAULT 'Ezy';
