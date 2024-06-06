/* Database design for the Match360.
Use PostgreSQL to create database objects

Author: Shidul Islam
Date: 10-11-2023
*/

-- Create the database --------------------------------------------------------------------------------------
-- CREATE DATABASE match360;

/* Create Schema */------------------------------------------------------------------------------------------
-- CREATE SCHEMA IF NOT EXISTS dbo;
-- CREATE SCHEMA IF NOT EXISTS users;
-- CREATE SCHEMA IF NOT EXISTS services;
-- CREATE SCHEMA IF NOT EXISTS admin;
-- CREATE SCHEMA IF NOT EXISTS vendors;

/* Create all types */---------------------------------------------------------------------------------------
-- -- Create religion type
-- CREATE TYPE users.religion_type AS ENUM ('muslim', 'hindu', 'buddhist', 'christian','sikh', 'jain','parsi');

-- -- Create community type
-- CREATE TYPE users.community_type AS ENUM ('Hindi', 'Panjabi', 'Bengali', 'Telugu', 'Sangha', 'crush');

-- -- Create country type
-- CREATE TYPE users.country_type AS ENUM (
--     'Bangladesh', 'India', 'Pakistan', 'Nepal', 'Bhutan', 'UAE', 'Saudi Arabia', 'Afghanistan', 'Insonesia');

-- -- Create occupation type
-- CREATE TYPE users.occupation_type AS ENUM (
--     'Defence', 'Civil Service', 'Software Engineer', 'Doctor', 'Civil Engineer', 'Engineer', 'Business Man', 'Private Servant', 'Pharmasist', 'Govt Servant', 'Teacher', 'Banker', 'Lawyer', 'Police', 'Freelancer', 'Politician', 'Unemployed', 'Student', 'Others'
-- );

-- -- Create gender type
-- CREATE TYPE users.gender_type AS ENUM (
--     'Male', 'Female', 'Other'
-- );

-- -- Create education type
-- CREATE TYPE users.education_type AS ENUM (
--     'MBBS', 'M.Sc', 'M.A','MBA', 'M.Com', 'M.E/M.Tech', 'LLM', 'B.E/B.Tech', 'M.S Engineer', 'Honours', 'B.Sc', 'B.Eng(Hons)', 'B.Bangla(Hons)', 'B.Sc(Pass)', 'B.A.(Pass)', 'B.Com(Pass)', 'BBA', 'LLB', 'Diploma', 'HSC', 'SSC', 'JSC/8', 'Pec/5', 'Uneduacated', 'Others'
-- );

-- -- Create language type
-- CREATE TYPE users.language_type AS ENUM (
--     'English', 'Bengali', 'Urdhu', 'Hindi', 'Arabic', 'Nepali', 'Bhutanese', 'Dari', 'Jawa', 'Others'
-- );

-- -- Marital status type
-- CREATE TYPE users.marital_status_type AS ENUM (
--     'Single', 'Divorced', 'Separated', 'Widow', 'Widower', 'Married'
-- );

-- -- Create message status type
-- CREATE TYPE users.message_status_type AS ENUM (
--     'active', 'inactive'
-- );

-- -- Dependent tables---------------------------------------------------------------------------------------

-- -- First create the independent tables ----------------------------------------------------------------------------

-- -- Create the users table
-- CREATE TABLE users.user(
-- <<<<<<< HEAD
-- <<<<<<< HEAD
-- =======
-- >>>>>>> Test
--     id serial PRIMARY KEY,
--     username VARCHAR(255) NOT NULL,
--     email VARCHAR(255) NOT NULL,
--     password_hash TEXT NOT NULL,
--     phone_number VARCHAR(20) NOT NULL,
--     photo VARCHAR(255),
--     educational_institution VARCHAR(255),
--     designation VARCHAR(255),
--     date_of_birth DATE,
--     religion users.religion_type DEFAULT 'muslim',
--     community users.community_type DEFAULT 'Hindi',
--     country users.country_type DEFAULT 'Bangladesh',
--     gender users.gender_type DEFAULT 'Male',
--     education users.education_type DEFAULT 'B.Sc',
--     occupation users.occupation_type DEFAULT 'Defence',
--     marital_status users.marital_status_type DEFAULT 'Single',
--     about_me VARCHAR(255),
--     created_at TIMESTAMP DEFAULT current_timestamp,
--     last_login_at TIMESTAMP DEFAULT NULL
-- <<<<<<< HEAD
-- =======
--     id serial PRIMARY KEY,
--     username VARCHAR(255) NOT NULL,
--     email VARCHAR(255) NOT NULL,
--     password_hash TEXT NOT NULL,
--     phone_number VARCHAR(20) NOT NULL,
--     photo VARCHAR(255),
--     date_of_birth DATE,
--     religion users.religion_type DEFAULT 'muslim',
--     community users.community_type DEFAULT 'Hindi',
--     country users.country_type DEFAULT 'Bangladesh',
--     gender users.gender_type DEFAULT 'Male',
--     education users.education_type DEFAULT 'B.Sc',
--     occupation users.occupation_type DEFAULT 'Defence',
--     about_me VARCHAR(255),
--     created_at TIMESTAMP DEFAULT current_timestamp,
--     last_login_at TIMESTAMP DEFAULT NULL
-- >>>>>>> origin/Test
-- =======
-- >>>>>>> Test
-- );

-- -- Create the users preference
-- CREATE TABLE users.user_preference(
-- <<<<<<< HEAD
-- <<<<<<< HEAD
-- =======
-- >>>>>>> Test
--     id serial PRIMARY KEY,
--     user_id INT NOT NULL UNIQUE,
--     from_age INT,
--     to_age INT,
--     desired_religion users.religion_type[] DEFAULT 'muslim',
--     desired_country users.country_type[] DEFAULT 'Bangladesh',
--     desired_community users.community_type[] DEFAULT 'Hindi',
--     desired_occupation users.occupation_type[] DEFAULT 'Defence',
--     desired_education users.education_type[] DEFAULT 'B.Sc',
--     desired_language users.language_type[] DEFAULT 'Bengali',
--     desired_gender users.gender_type[] DEFAULT 'Male',
--     desired_marital_status users.gender_type[] DEFAULT 'Male',
--     created_at TIMESTAMP DEFAULT current_timestamp,
--     FOREIGN KEY (user_id) REFERENCES users.user(id)
-- <<<<<<< HEAD
-- =======
--     id serial PRIMARY KEY,
--     user_id INT NOT NULL UNIQUE,
--     from_age INT,
--     to_age INT,
--     desired_religion users.religion_type[] DEFAULT 'muslim',
--     desired_country users.country_type[] DEFAULT 'Bangladesh',
--     desired_community users.community_type[] DEFAULT 'Hindi',
--     desired_occupation users.occupation_type[] DEFAULT 'Defence',
--     desired_education users.education_type[] DEFAULT 'B.Sc',
--     desired_language users.language_type[] DEFAULT 'Bengali',
--     desired_gender users.gender_type[] DEFAULT 'Male',
--     desired_marital_status users.gender_type[] DEFAULT 'Male',
--     created_at TIMESTAMP DEFAULT current_timestamp,
--     FOREIGN KEY (user_id) REFERENCES users.user(id)
-- >>>>>>> origin/Test
-- =======
-- >>>>>>> Test
-- );
-- Create the database --------------------------------------------------------------------------------------
-- CREATE DATABASE match360;

/* Create Schema */------------------------------------------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS dbo;
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS services;
CREATE SCHEMA IF NOT EXISTS admin;
CREATE SCHEMA IF NOT EXISTS vendors;

/* Create all types */---------------------------------------------------------------------------------------
-- Create religion type
CREATE TYPE users.religion_type AS ENUM ('muslim', 'hindu', 'buddhist', 'christian', 'sikh', 'parsi', 'jain');

-- Create community type
CREATE TYPE users.community_type AS ENUM ('Hindi', 'Panjabi', 'Bengali', 'Telugu');

-- Create country type
CREATE TYPE users.country_type AS ENUM ('Bangladesh', 'India', 'Pakistan', 'Nepal', 'Bhutan', 'UAE', 'Saudi Arabia', 'Afghanistan', 'Insonesia');

-- Create occupation type
CREATE TYPE users.occupation_type AS ENUM (
    'Defence', 'Civil Service', 'Software Engineer', 'Doctor', 'Civil Engineer', 'Others'
);

-- Create gender type
CREATE TYPE users.gender_type AS ENUM (
    'Male', 'Female', 'Other'
);

-- Create education type
CREATE TYPE users.education_type AS ENUM (
    'B.E/B.Tech', 'M.E/M.Tech', 'M.S Engineer', 'B.Sc', 'M.Sc', 'B.Eng(Hons)', 'B.Bangla(Hons)', 'Others'
);

-- Create language type
CREATE TYPE users.language_type AS ENUM (
    'English', 'Bengali', 'Urdhu', 'Hindi', 'Others'
);

-- Create message status type
CREATE TYPE users.message_status_type AS ENUM (
    'active', 'inactive'
);

-- First create the independent tables ----------------------------------------------------------------------------

-- Create the users table
CREATE TABLE users.user(
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Test
    id serial PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    photo VARCHAR(255),
    date_of_birth DATE,
    religion users.religion_type DEFAULT 'muslim',
    community users.community_type DEFAULT 'Hindi',
    country users.country_type DEFAULT 'Bangladesh',
    gender users.gender_type DEFAULT 'Male',
    education users.education_type DEFAULT 'B.Sc',
    occupation users.occupation_type DEFAULT 'Defence',
    about_me VARCHAR(255),
    created_at TIMESTAMP DEFAULT current_timestamp,
    last_login_at TIMESTAMP DEFAULT NULL
<<<<<<< HEAD
=======
    id serial PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    photo VARCHAR(255),
    date_of_birth DATE,
    religion users.religion_type DEFAULT 'muslim',
    community users.community_type DEFAULT 'Hindi',
    country users.country_type DEFAULT 'Bangladesh',
    gender users.gender_type DEFAULT 'Male',
    education users.education_type DEFAULT 'B.Sc',
    occupation users.occupation_type DEFAULT 'Defence',
    about_me VARCHAR(255),
    created_at TIMESTAMP DEFAULT current_timestamp,
    last_login_at TIMESTAMP DEFAULT NULL
>>>>>>> origin/Test
=======
>>>>>>> Test
);

-- Dependent tables---------------------------------------------------------------------------------------

-- Create the user_preference table
CREATE TABLE users.user_preference(
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Test
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    from_age INT,
    to_age INT,
    desired_religion users.religion_type[] DEFAULT 'muslim',
    desired_country users.country_type[] DEFAULT 'Bangladesh',
    desired_community users.community_type[] DEFAULT 'Hindi',
    desired_occupation users.occupation_type[] DEFAULT 'Defence',
    desired_education users.education_type[] DEFAULT 'B.Sc',
    desired_language users.language_type[] DEFAULT 'Bengali',
    desired_gender users.gender_type[] DEFAULT 'Male',
    desired_marital_status users.gender_type[] DEFAULT 'Male',
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users.user(id)
<<<<<<< HEAD
=======
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    from_age INT,
    to_age INT,
    desired_religion users.religion_type[] DEFAULT 'muslim',
    desired_country users.country_type[] DEFAULT 'Bangladesh',
    desired_community users.community_type[] DEFAULT 'Hindi',
    desired_occupation users.occupation_type[] DEFAULT 'Defence',
    desired_education users.education_type[] DEFAULT 'B.Sc',
    desired_language users.language_type[] DEFAULT 'Bengali',
    desired_gender users.gender_type[] DEFAULT 'Male',
    desired_marital_status users.gender_type[] DEFAULT 'Male',
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users.user(id)
>>>>>>> origin/Test
=======
>>>>>>> Test
);


-- Create feedback table
CREATE TABLE users.feedback (
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    feedback_text VARCHAR(255),
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users.user(id)
);

-- Create feedback table
CREATE TABLE users.feedback (
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    feedback_text VARCHAR(255),
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users.user(id)
);


-- Create matches table
CREATE TABLE users.matches (
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    matched_user_id INT NOT NULL UNIQUE,
    match_score INT,
    date_of_match DATE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users.user(id),
    FOREIGN KEY (matched_user_id) REFERENCES users.user(id)
);

-- Create blocked_profile table
CREATE TABLE users.blocked_profiles (
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    blocked_user_id INT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users.user(id),
    FOREIGN KEY (blocked_user_id) REFERENCES users.user(id)
);

-- Create messages table
CREATE TABLE users.messages (
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    title VARCHAR(255),
    body VARCHAR(255),
    status users.message_status_type DEFAULT 'active',
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users.user(id)
);

-- Create subscription table
CREATE TABLE users.subscription (
    id serial PRIMARY KEY,
    title VARCHAR(255),
    validity INT,
    price INT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

-- Create subscription table
CREATE TABLE users.user_subscription (
    id serial PRIMARY KEY,
    subscription_id INT NOT NULL UNIQUE,
    user_discount INT,
    subscribed_on INT,
    expiry_date INT,
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (subscription_id) REFERENCES users.subscription(id)
);

-- Create success stories table
CREATE TABLE users.success_stories ( 
    id serial PRIMARY KEY,
    bride_id INT NOT NULL UNIQUE,
    groom_id INT NOT NULL UNIQUE,
    marriage_date DATE,
    created_at TIMESTAMP DEFAULT current_timestamp
);

-- add to short list table
CREATE TABLE users.favourite_list (
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    favourite_id INT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users.user(id) 
);

-- Create App Monitoring table
CREATE TABLE dbo.app_monitor_logs (
    id serial PRIMARY KEY,
    page_name VARCHAR(255),
    loading_time FLOAT,
    procedure_execution_time FLOAT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

-- Create Logging table
CREATE TABLE dbo.app_logs (
    id serial PRIMARY KEY,
    level VARCHAR(10),
    message TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

-- Create Exception Handling table
CREATE TABLE dbo.exception_logs (
    id serial PRIMARY KEY,
    exception_type VARCHAR(10),
    exception_message TEXT,
    line_number INT,
    stack_trace TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

-- Create Audit trail table
CREATE TABLE dbo.audit_trail (
    id serial PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    action VARCHAR(255),
    details JSONB,
    created_at TIMESTAMP DEFAULT current_timestamp
    FOREIGN KEY (user_id) REFERENCES users.user(id)
);

-- Create Audit trail table
CREATE TABLE dbo.email_OTP (
    id serial PRIMARY KEY,
    hashedOtp VARCHAR(255),
    email VARCHAR(255),
    tried INT,
    type VARCHAR(255),
    matched INT,
    created_at TIMESTAMP DEFAULT current_timestamp
);
--- profile views --- 
<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS users.profile_views
(
    id integer NOT NULL DEFAULT nextval('users.profile_views_id_seq'::regclass),
    viewer_id integer,
    viewed_profile_id integer,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT profile_views_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;
ALTER TABLE IF EXISTS users.profile_views
    OWNER to postgres;
=======
CREATE TABLE users.profile_views
(
    id serial PRIMARY KEY,
    viewer_id integer,
    viewed_profile_id integer,
    created_at TIMESTAMP DEFAULT current_timestamp
)
>>>>>>> origin/Test

CREATE TABLE dbo.notice (
    id SERIAL PRIMARY KEY,
    notice_title VARCHAR(255) NOT NULL,
    notice_topics VARCHAR(255),
    notice_file VARCHAR(255)
);

------------------------------------------------ vendors tables----------------------------------------------------

----------------------------------  Topics : vendor tables type (city,country,business), Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------

-- Create city type
CREATE TYPE vendors.city_type AS ENUM ('Dhaka', 'Barishal', 'Sylhet', 'Chittagong', 'Khulna', 'Rajshahi', 'Mymensingh', 'Cumilla', 'Noakhali','Others');
-- Create country type
CREATE TYPE vendors.country_type AS ENUM ('Bangladesh', 'India', 'Pakistan', 'Nepal', 'Bhutan', 'UAE', 'Saudi Arabia', 'Afghanistan', 'Insonesia', 'USA' ,'UK');
-- Create business type
CREATE TYPE vendors.business_type AS ENUM ('Photography', 'Catering', 'Music Band', 'Outdoor venue', 'Indoor Venue','Cake','Beauty and Makeup');

CREATE TYPE vendors.profile_status AS ENUM ('pending', 'verified', 'blocked');

---------------------------------  Topics : vendor table with all field , Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------

CREATE TABLE vendors.vendor(
    id serial PRIMARY KEY,
    org_name VARCHAR(255) NOT NULL,
    org_username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    photo VARCHAR(255),
    address VARCHAR(255) NOT NULL, 
    city vendors.city_type DEFAULT 'Dhaka',
    country vendors.country_type DEFAULT 'Bangladesh',
    business_category vendors.business_type DEFAULT 'Photography',
    details VARCHAR(255),
    tin_certificate VARCHAR(255);
    created_at TIMESTAMP DEFAULT current_timestamp,
    last_login_at TIMESTAMP DEFAULT NULL,
    vendor_status BOOLEAN DEFAULT FALSE,
    vendor_profile_status vendors.profile_status DEFAULT 'pending'
);

----------------------------------  Topics : notice table for vendor dashboard, Author: Md. Iquball Hossain, Date: 29-11-2023 ---------------

CREATE TABLE admin.vendor_notice (
    id SERIAL PRIMARY KEY,
    vendor_id INT,
    admin_id INT,
    notice_title VARCHAR(255),
    notice_topics TEXT,
    notice_file VARCHAR(255),
    notice_time TIMESTAMP DEFAULT current_timestamp
);

----------------------------------  Topics : Helpdesh for vendor dashboard, Author: Md. Iquball Hossain, Date: 04-11-2023 -------------------

CREATE TYPE vendors.status_type AS ENUM ('pending', 'inprogress', 'solved');

CREATE TABLE vendors.helpdesk (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER
    admin_role VARCHAR(50),
    vendor_id INTEGER NOT NULL,
    problem_topics TEXT,
    problem_file TEXT,
    message_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    problem_status vendors.status_type 'pending'
);

----------------------------------  Topics : Helpdesh for vendor dashboard, Author: Md. Iquball Hossain, Date: 04-11-2023 ---------------------
CREATE TABLE admin.admin_profile (
    admin_id SERIAL PRIMARY KEY,
    admin_username VARCHAR(100) UNIQUE NOT NULL,
    admin_email VARCHAR(100) UNIQUE NOT NULL,
    admin_password VARCHAR(255) NOT NULL,
    admin_phone VARCHAR(20),
    admin_role VARCHAR(50),
    admin_role_id INT,
    admin_role_category VARCHAR(100),
    admin_photo VARCHAR(255),
    admin_create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    admin_last_login_time TIMESTAMP,
    admin_status BOOLEAN DEFAULT True
);

----------------------------------  Topics : vendor_service table for vendor dashboard, Author: Md. Iquball Hossain, Date: 17-12-2023 ----------

CREATE TABLE vendors.vendor_service (
    vendor_service_id SERIAL PRIMARY KEY,
    vendor_id INT REFERENCES vendors.vendor(id) ON DELETE CASCADE,
    admin_id INT REFERENCES admin.admin_profile(admin_id) ON DELETE CASCADE,
    business_category_name VARCHAR(100),
    business_type VARCHAR(100),
    guest_capacity INT,
    pricing_file VARCHAR(255),
    social_media_facebook VARCHAR(100),
    social_media_instagram VARCHAR(100),
    website_url VARCHAR(100),
    whatsapp VARCHAR(100),
    org_history VARCHAR(350),
    org_location_details VARCHAR(230),
    org_previous_work_details VARCHAR(600),
    org_top_work_details VARCHAR(500),
    org_available_services VARCHAR(500),
    org_best_sites VARCHAR(500),
    award_affiliation VARCHAR(500),
    office_start_time VARCHAR(500),
    office_closed_time VARCHAR(500),
    office_holiday VARCHAR(100),
    office_break_time VARCHAR(100),
    offering_venue VARCHAR(400),
    ceremony_type VARCHAR(500),
    offering_service VARCHAR(600),
    others VARCHAR(500),
    vendor_service_status BOOLEAN,
    created_time TIMESTAMP,
    last_edited_time TIMESTAMP
);

----------------------------------  Topics : user_service table for vendor dashboard, Author: Md. Iquball Hossain, Date: 17-12-2023 -------------

CREATE TABLE services.user_service (
    user_service_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users.user(id) ON DELETE CASCADE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20), 
    ceremony_date DATE,
    ceremony_time VARCHAR(30),
    program_duration VARCHAR(300),
    number_of_guest INT,
    about_ceremony VARCHAR(500),
    wanted_service VARCHAR(500),
    wanted_venues VARCHAR(400),
    request_status BOOLEAN,
    request_time TIMESTAMP,
    last_edited_time TIMESTAMP
);

