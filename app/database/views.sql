/* Database design for the Match360.
Use PostgreSQL to create database objects

Author: Shidul Islam
Date: 10-11-2023
*/

-- Create the database --------------------------------------------------------------------------------------
-- CREATE DATABASE match360;

/*===================== USER Schema ======================*/ 

-- View: users.user_view

-- DROP VIEW users.user_view;

CREATE OR REPLACE VIEW users.user_view
   AS
   SELECT id,
      username,
      email,
      phone_number,
      date_of_birth
   FROM users."user";

ALTER TABLE users.user_view
      OWNER TO postgres;


-- View: users.recent_view_data_view

-- DROP VIEW users.recent_view_data_view;

CREATE OR REPLACE VIEW users.recent_view_data_view
   AS
   SELECT id,
      username,
      email,
      phone_number,
      photo,
      date_of_birth,
      religion,
      community,
      country,
      gender,
      education,
      occupation,
      language,
      about_me
   FROM users.get_recent_view_data(123) get_recent_view_data(id, username, email, phone_number, photo, date_of_birth, religion, community, country, gender, education, occupation, language, about_me);

ALTER TABLE users.recent_view_data_view
   OWNER TO postgres;


----- Email OTP -----

CREATE OR REPLACE VIEW dbo.email_otp_view
   AS
   SELECT id,
      email,
      tried,
      type,
      matched,
      created_at,
      hashedotp
   FROM dbo.email_otp;

ALTER TABLE dbo.email_otp_view
      OWNER TO postgres;


