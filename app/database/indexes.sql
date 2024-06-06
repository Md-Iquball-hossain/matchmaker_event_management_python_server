/* Database design for the Match360.
Use PostgreSQL to create database objects

Author: Shidul Islam
Date: 10-11-2023
*/

-- Create the database --------------------------------------------------------------------------------------
-- CREATE DATABASE match360;


/* USERS SCHEMA */
--Indexing the user table
CREATE INDEX idx_users_country ON users.user(country);
CREATE INDEX idx_users_religion ON users.user(religion);
CREATE INDEX idx_users_occupation ON users.user(occupation);

