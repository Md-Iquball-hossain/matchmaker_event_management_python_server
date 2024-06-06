/* Database design for the Match360.
Use PostgreSQL to create database objects

Author: Shidul Islam
Date: 10-11-2023
*/

-- Create the database --------------------------------------------------------------------------------------
-- CREATE DATABASE match360;

/*===================== USER Schema ======================*/ 

-- Create user function 
-- FUNCTION: users.insert_user(character varying, character varying, text, character varying, character varying, date, users.religion_type, users.community_type, users.country_type, users.gender_type, users.education_type, users.occupation_type, character varying, timestamp without time zone)

-- DROP FUNCTION IF EXISTS users.insert_user(character varying, character varying, text, character varying, character varying, date, users.religion_type, users.community_type, users.country_type, users.gender_type, users.education_type, users.occupation_type, character varying, timestamp without time zone);

CREATE OR REPLACE FUNCTION users.insert_user(
	p_username character varying,
	p_email character varying,
	p_password_hash text,
	p_phone_number character varying,
	p_photo character varying,
	p_date_of_birth date,
	p_religion users.religion_type,
	p_community users.community_type,
	p_country users.country_type,
	p_gender users.gender_type,
	p_education users.education_type,
	p_occupation users.occupation_type,
	p_about_me character varying,
	p_last_login_at timestamp without time zone)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    INSERT INTO users."user"(
        username, email, password_hash, phone_number, photo, date_of_birth, religion, community,
        country, gender, education, occupation, about_me, last_login_at
    ) VALUES (
        p_username, p_email, p_password_hash, p_phone_number, p_photo, p_date_of_birth, p_religion,
        p_community, p_country, p_gender, p_education, p_occupation, p_about_me, p_last_login_at
    );
END;
$BODY$;

ALTER FUNCTION users.insert_user(character varying, character varying, text, character varying, character varying, date, users.religion_type, users.community_type, users.country_type, users.gender_type, users.education_type, users.occupation_type, character varying, timestamp without time zone)
    OWNER TO postgres;


-- User preference Matching Profile
-- FUNCTION: users.get_matching_profiles(users.religion_type, users.community_type, users.country_type, users.language_type, users.gender_type)

-- DROP FUNCTION IF EXISTS users.get_matching_profiles(users.religion_type, users.community_type, users.country_type, users.language_type, users.gender_type);

CREATE OR REPLACE FUNCTION users.get_matching_profiles(
	p_desired_religion users.religion_type,
	p_desired_community users.community_type,
	p_desired_country users.country_type,
	p_desired_language users.language_type,
	p_user_preference_male_or_female users.gender_type)
    RETURNS TABLE(username character varying, email character varying, phone_number character varying, photo character varying, date_of_birth date, religion users.religion_type, community users.community_type, country users.country_type, gender users.gender_type, education users.education_type, occupation users.occupation_type, language users.language_type, about_me character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        u.username,
        u.email,
        u.phone_number,
        u.photo,
        u.date_of_birth,
        u.religion,
        u.community,
        u.country,
        u.gender,
        u.education,
        u.occupation,
        u.language,
        u.about_me
    FROM users.user AS u
    WHERE
        u.religion = p_desired_religion
        AND u.community = p_desired_community
        AND u.country = p_desired_country
        AND u.language = p_desired_language
        AND (
            (p_user_preference_male_or_female = 'Male' AND u.gender = 'Female')
            OR (p_user_preference_male_or_female = 'Female' AND u.gender = 'Male')
        );
END;
$BODY$;

ALTER FUNCTION users.get_matching_profiles(users.religion_type, users.community_type, users.country_type, users.language_type, users.gender_type)
    OWNER TO postgres;


-- insert_user_preference function --
-- FUNCTION: users.insert_user_preference(integer, integer, integer, text[], text[], text[], text[], text[], text[], text[], text[])

-- DROP FUNCTION IF EXISTS users.insert_user_preference(integer, integer, integer, text[], text[], text[], text[], text[], text[], text[], text[]);

CREATE OR REPLACE FUNCTION users.insert_user_preference(
	p_user_id integer,
	p_from_age integer,
	p_to_age integer,
	p_desired_religion text[],
	p_desired_country text[],
	p_desired_community text[],
	p_desired_occupation text[],
	p_desired_education text[],
	p_desired_language text[],
	p_desired_gender text[],
	p_desired_marital_status text[])
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    INSERT INTO users.user_preference(
        user_id, from_age, to_age, desired_religion, desired_country, desired_community,
        desired_occupation, desired_education, desired_language, desired_gender, desired_marital_status
    ) VALUES (
        p_user_id, p_from_age, p_to_age,
        ARRAY[p_desired_religion]::users.religion_type[],
        ARRAY[p_desired_country]::users.country_type[],
        ARRAY[p_desired_community]::users.community_type[],
        ARRAY[p_desired_occupation]::users.occupation_type[],
        ARRAY[p_desired_education]::users.education_type[],
        ARRAY[p_desired_language]::users.language_type[],
        ARRAY[p_desired_gender]::users.gender_type[],
        ARRAY[p_desired_marital_status]::users.marital_status_type[]
    );
END;
$BODY$;

ALTER FUNCTION users.insert_user_preference(integer, integer, integer, text[], text[], text[], text[], text[], text[], text[], text[])
    OWNER TO postgres;


-- user_preference function --
-- FUNCTION: users.user_preference(integer, integer, integer, users.religion_type, users.country_type, users.community_type, users.occupation_type, users.education_type, users.language_type, users.gender_type)

-- DROP FUNCTION IF EXISTS users.user_preference(integer, integer, integer, users.religion_type, users.country_type, users.community_type, users.occupation_type, users.education_type, users.language_type, users.gender_type);

CREATE OR REPLACE FUNCTION users.user_preference(
	user_id integer,
	from_age integer,
	to_age integer,
	desired_religion users.religion_type,
	desired_country users.country_type,
	desired_community users.community_type,
	desired_occupation users.occupation_type,
	desired_education users.education_type,
	desired_language users.language_type,
	desired_gender users.gender_type)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    INSERT INTO users.user_preference (
        user_id, from_age, to_age, desired_religion, desired_country,
        desired_community, desired_occupation, desired_education,
        desired_language, desired_gender
    )
    VALUES (
        user_id, from_age, to_age, desired_religion, desired_country,
        desired_community, desired_occupation, desired_education,
        desired_language, desired_gender
    );
END;
$BODY$;

ALTER FUNCTION users.user_preference(integer, integer, integer, users.religion_type, users.country_type, users.community_type, users.occupation_type, users.education_type, users.language_type, users.gender_type)
    OWNER TO postgres;



-- update_user_preferences function --
CREATE OR REPLACE FUNCTION users.update_user_preferences(
	p_user_id integer,
	new_desired_religion users.religion_type DEFAULT NULL::users.religion_type,
	new_desired_country users.country_type DEFAULT NULL::users.country_type,
	new_desired_community users.community_type DEFAULT NULL::users.community_type,
	new_desired_occupation users.occupation_type DEFAULT NULL::users.occupation_type,
	new_desired_education users.education_type DEFAULT NULL::users.education_type,
	new_desired_language users.language_type DEFAULT NULL::users.language_type,
	new_desired_gender users.gender_type DEFAULT NULL::users.gender_type,
	new_from_age integer DEFAULT NULL::integer,
	new_to_age integer DEFAULT NULL::integer)
    RETURNS TABLE(id integer, desired_religion users.religion_type, desired_country users.country_type, desired_community users.community_type, desired_occupation users.occupation_type, desired_education users.education_type, desired_language users.language_type, desired_gender users.gender_type, from_age integer, to_age integer) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    -- Update user preferences including age range
    UPDATE users.user_preference
    SET
        desired_religion = COALESCE(new_desired_religion, desired_religion),
        desired_country = COALESCE(new_desired_country, desired_country),
        desired_community = COALESCE(new_desired_community, desired_community),
        desired_occupation = COALESCE(new_desired_occupation, desired_occupation),
        desired_education = COALESCE(new_desired_education, desired_education),
        desired_language = COALESCE(new_desired_language, desired_language),
        desired_gender = COALESCE(new_desired_gender, desired_gender),
        from_age = COALESCE(new_from_age, from_age),
        to_age = COALESCE(new_to_age, to_age)
    WHERE users.user_preference.id = p_user_id
    RETURNING *;
END;
$BODY$;

ALTER FUNCTION users.update_user_preferences(integer, users.religion_type, users.country_type, users.community_type, users.occupation_type, users.education_type, users.language_type, users.gender_type, integer, integer)
    OWNER TO postgres;

-- Add to favourite list
-- FUNCTION: users.add_to_favourite_list(integer, integer, boolean)

-- DROP FUNCTION IF EXISTS users.add_to_favourite_list(integer, integer, boolean);

CREATE OR REPLACE FUNCTION users.add_to_favourite_list(
	user_id integer DEFAULT NULL::integer,
	favourite_id integer DEFAULT NULL::integer,
	favourite boolean DEFAULT false)
    RETURNS boolean
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    insertion_status boolean := FALSE;
BEGIN
    IF user_id IS NULL THEN
        user_id := 0;
    END IF;
    IF favourite_id IS NULL THEN
        favourite_id := 0;
    END IF;
    BEGIN
        IF user_id IS NOT NULL AND favourite_id IS NOT NULL THEN
            INSERT INTO users.favourite_list (user_id, favourite_id, is_favourite)
            VALUES (user_id, favourite_id, favourite);
            insertion_status := TRUE;
            RAISE NOTICE 'Insertion successful';
        ELSE
            RAISE NOTICE 'Both user_id and favourite_id are required parameters';
        END IF;
    EXCEPTION
        WHEN others THEN
            RAISE NOTICE 'Error in add_to_favourite_list: %', SQLERRM;
    END;
    RETURN insertion_status;
END;
$BODY$;

ALTER FUNCTION users.add_to_favourite_list(integer, integer, boolean)
    OWNER TO postgres;



--- get near me function ---
-- FUNCTION: users.get_near_me_profiles(users.country_type, users.gender_type)

-- DROP FUNCTION IF EXISTS users.get_near_me_profiles(users.country_type, users.gender_type);

CREATE OR REPLACE FUNCTION users.get_near_me_profiles(
	p_desired_country users.country_type,
	p_user_preference_male_or_female users.gender_type)
    RETURNS TABLE(id integer, username character varying, email character varying, phone_number character varying, photo character varying, date_of_birth date, religion users.religion_type, community users.community_type, country users.country_type, gender users.gender_type, education users.education_type, occupation users.occupation_type, language users.language_type, about_me character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
		u.id,
        u.username,
        u.email,
        u.phone_number,
        u.photo,
        u.date_of_birth,
        u.religion,
        u.community,
        u.country,
        u.gender,
        u.education,
        u.occupation,
        u.language,
        u.about_me
    FROM users.user AS u
    WHERE
        u.country = p_desired_country
        AND (
            (p_user_preference_male_or_female = 'Male' AND u.gender = 'Female')
            OR (p_user_preference_male_or_female = 'Female' AND u.gender = 'Male')
        );
END;
$BODY$;

ALTER FUNCTION users.get_near_me_profiles(users.country_type, users.gender_type)
    OWNER TO postgres;

--- get near me function with favourite previous---
-- FUNCTION: users.get_near_me_profiles_with_favourites(users.country_type, users.gender_type, integer)

-- DROP FUNCTION IF EXISTS users.get_near_me_profiles_with_favourites(users.country_type, users.gender_type, integer);

CREATE OR REPLACE FUNCTION users.get_near_me_profiles_with_favourites(
	p_desired_country users.country_type,
	p_user_preference_male_or_female users.gender_type,
	p_user_id integer)
    RETURNS TABLE(id integer, username character varying, email character varying, phone_number character varying, photo character varying, date_of_birth date, religion users.religion_type, community users.community_type, country users.country_type, gender users.gender_type, education users.education_type, occupation users.occupation_type, language users.language_type, about_me character varying, is_favourite boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        u.id,
        u.username,
        u.email,
        u.phone_number,
        u.photo,
        u.date_of_birth,
        u.religion,
        u.community,
        u.country,
        u.gender,
        u.education,
        u.occupation,
        u.language,
        u.about_me,
        fl.is_favourite -- Return is_favourite column directly
    FROM users.user AS u
    LEFT JOIN users.favourite_list AS fl 
        ON fl.favourite_id = u.id
    WHERE
        u.country = p_desired_country
        AND (
            (p_user_preference_male_or_female = 'Male' AND u.gender = 'Female')
            OR (p_user_preference_male_or_female = 'Female' AND u.gender = 'Male')
        );
END;
$BODY$;

ALTER FUNCTION users.get_near_me_profiles_with_favourites(users.country_type, users.gender_type, integer)
    OWNER TO postgres;


--- get user matching profiles previous----
-- FUNCTION: users.get_user_matching_profiles(users.religion_type, users.community_type, users.country_type, users.language_type, users.gender_type, integer)

-- DROP FUNCTION IF EXISTS users.get_user_matching_profiles(users.religion_type, users.community_type, users.country_type, users.language_type, users.gender_type, integer);

CREATE OR REPLACE FUNCTION users.get_user_matching_profiles(
	p_desired_religion users.religion_type,
	p_desired_community users.community_type,
	p_desired_country users.country_type,
	p_desired_language users.language_type,
	p_user_preference_male_or_female users.gender_type,
	p_user_id integer)
    RETURNS TABLE(id integer, username character varying, email character varying, phone_number character varying, photo character varying, date_of_birth date, religion users.religion_type, community users.community_type, country users.country_type, gender users.gender_type, education users.education_type, occupation users.occupation_type, language users.language_type, about_me character varying, is_favourite boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        u.id,
        u.username,
        u.email,
        u.phone_number,
        u.photo,
        u.date_of_birth,
        u.religion,
        u.community,
        u.country,
        u.gender,
        u.education,
        u.occupation,
        u.language,
        u.about_me,
        fl.is_favourite
    FROM 
        users.user AS u
    LEFT JOIN 
        users.favourite_list AS fl 
        ON fl.favourite_id = u.id
    WHERE
        u.religion = p_desired_religion
        AND u.community = p_desired_community
        AND u.country = p_desired_country
        AND u.language = p_desired_language
        AND (
            (p_user_preference_male_or_female = 'Male' AND u.gender = 'Female')
            OR (p_user_preference_male_or_female = 'Female' AND u.gender = 'Male')
        );
END;
$BODY$;

ALTER FUNCTION users.get_user_matching_profiles(users.religion_type, users.community_type, users.country_type, users.language_type, users.gender_type, integer)
    OWNER TO postgres;



--- tadays match previous---
-- FUNCTION: users.get_user_todays_match(integer, users.country_type, users.language_type, users.gender_type)

-- DROP FUNCTION IF EXISTS users.get_user_todays_match(integer, users.country_type, users.language_type, users.gender_type);

CREATE OR REPLACE FUNCTION users.get_user_todays_match(
	p_user_id integer,
	p_desired_country users.country_type,
	p_desired_language users.language_type,
	p_user_preference_gender users.gender_type)
    RETURNS TABLE(id integer, username character varying, email character varying, phone_number character varying, photo character varying, date_of_birth date, religion users.religion_type, country users.country_type, gender users.gender_type, education users.education_type, occupation users.occupation_type, language users.language_type, about_me character varying, is_favourite boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        u.id,
        u.username,
        u.email,
        u.phone_number,
        u.photo,
        u.date_of_birth,
        u.religion,
        u.country,
        u.gender,
        u.education,
        u.occupation,
        u.language,
        u.about_me,
        fl.user_id IS NOT NULL AS is_favourite -- Return is_favourite column directly
    FROM users.user AS u
    LEFT JOIN users.favourite_list AS fl 
        ON fl.favourite_id = u.id
    WHERE
        u.country = p_desired_country
        AND u.language = p_desired_language
        AND (
            (p_user_preference_gender = 'Male' AND u.gender = 'Female')
            OR (p_user_preference_gender = 'Female' AND u.gender = 'Male')
        )
        AND u.created_at::date = CURRENT_DATE;
END;
$BODY$;

ALTER FUNCTION users.get_user_todays_match(integer, users.country_type, users.language_type, users.gender_type)
    OWNER TO postgres;


-- Recent view data
-- FUNCTION: users.get_recent_view_data(integer)

-- DROP FUNCTION IF EXISTS users.get_recent_view_data(integer);

CREATE OR REPLACE FUNCTION users.get_recent_view_data(
	p_viewer_id integer)
    RETURNS TABLE(id integer, username character varying, email character varying, phone_number character varying, photo character varying, date_of_birth date, religion users.religion_type, community users.community_type, country users.country_type, gender users.gender_type, education users.education_type, occupation users.occupation_type, language users.language_type, about_me character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        u.id,
        u.username,
        u.email,
        u.phone_number,
        u.photo,
        u.date_of_birth,
        u.religion,
        u.community,
        u.country,
        u.gender,
        u.education,
        u.occupation,
        u.language,
        u.about_me
    FROM users.user AS u
    JOIN users.profile_views AS pv ON u.id = pv.viewed_profile_id
    WHERE
        pv.viewer_id = p_viewer_id
        AND u.id != p_viewer_id;  -- Exclude the viewer's own profile
END;
$BODY$;

ALTER FUNCTION users.get_recent_view_data(integer)
    OWNER TO postgres;

--- get user with preference
-- FUNCTION: users.get_user_with_preferences(integer)

-- DROP FUNCTION IF EXISTS users.get_user_with_preferences(integer);

CREATE OR REPLACE FUNCTION users.get_user_with_preferences(
	user_id_param integer)
    RETURNS TABLE(user_data json, user_preference_data json) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        json_build_object(
            'user_id', u.id,
            'username', u.username,
            'email', u.email,
            'about_me', u.about_me,
            'community', u.community,
            'country', u.country,
            'date_of_birth', u.date_of_birth,
            'education', u.education,
            'gender', u.gender,
            'language', u.language,
            'occupation', u.occupation,
            'phone_number', u.phone_number,
            'photo', u.photo,
            'religion', u.religion
        ) AS user_data,
        json_build_object(
            'from_age', up.from_age,
            'to_age', up.to_age,
            'desired_religion', up.desired_religion,
            'desired_country', up.desired_country,
            'desired_community', up.desired_community,
            'desired_occupation', up.desired_occupation,
            'desired_education', up.desired_education,
            'desired_language', up.desired_language,
            'desired_marital_status', up.desired_marital_status,
            'desired_gender', up.desired_gender
        ) AS user_preference_data
    FROM
        users.user u
    LEFT JOIN
        users.user_preference up ON u.id = up.user_id
    WHERE
        u.id = user_id_param;

END;
$BODY$;

ALTER FUNCTION users.get_user_with_preferences(integer)
    OWNER TO postgres;

--- Save profile view
CREATE OR REPLACE FUNCTION users.save_profile_view(
	p_viewer_id integer,
	p_viewed_profile_id integer)
    RETURNS boolean
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    -- Insert the data into the profile_views table
    BEGIN
        INSERT INTO users.profile_views (viewer_id, viewed_profile_id, timestamp)
        VALUES (p_viewer_id, p_viewed_profile_id, NOW() + INTERVAL '72 hours');

        -- Return TRUE if the insertion was successful
        RETURN TRUE;
    EXCEPTION
        WHEN others THEN
            -- Log the error details
            RAISE NOTICE 'Error in save_profile_view: %', SQLERRM;
            RAISE NOTICE 'Details: viewer_id=%, viewed_profile_id=%', p_viewer_id, p_viewed_profile_id;
            RETURN FALSE;
    END;
END;
$BODY$;

ALTER FUNCTION users.save_profile_view(integer, integer)
    OWNER TO postgres;


--- User Preference ---
CREATE OR REPLACE FUNCTION users.user_preference(
	user_id integer,
	from_age integer,
	to_age integer,
	desired_religion users.religion_type,
	desired_country users.country_type,
	desired_community users.community_type,
	desired_occupation users.occupation_type,
	desired_education users.education_type,
	desired_language users.language_type,
	desired_gender users.gender_type)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    INSERT INTO users.user_preference (
        user_id, from_age, to_age, desired_religion, desired_country,
        desired_community, desired_occupation, desired_education,
        desired_language, desired_gender
    )
    VALUES (
        user_id, from_age, to_age, desired_religion, desired_country,
        desired_community, desired_occupation, desired_education,
        desired_language, desired_gender
    );
END;
$BODY$;

ALTER FUNCTION users.user_preference(integer, integer, integer, users.religion_type, users.country_type, users.community_type, users.occupation_type, users.education_type, users.language_type, users.gender_type)
    OWNER TO postgres;

/*===================== DBO Schema ======================*/ 

--- email otp ---
CREATE OR REPLACE FUNCTION dbo.call_email_otp(
	email character varying,
	otp_type character varying,
	minute integer,
	matched boolean)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    -- Insert data into the 'dbo.email_otp' table
    INSERT INTO dbo.email_otp (email, type, tried, matched)
    VALUES (email, otp_type, minute, matched);
END;
$BODY$;

ALTER FUNCTION dbo.call_email_otp(character varying, character varying, integer, boolean)
    OWNER TO postgres;

--- create email otp --- 
CREATE OR REPLACE FUNCTION dbo.create_email_otp(
	hashed_otp_param bytea,
	email_param text,
	type_param text)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    -- Insert data into the 'dbo.email_otp' table
    INSERT INTO dbo.email_otp (hashedotp, email, type)
    VALUES (hashed_otp_param, email_param, type_param);
END;
$BODY$;

ALTER FUNCTION dbo.create_email_otp(bytea, text, text)
    OWNER TO postgres;


--- get email OTP ---
CREATE OR REPLACE FUNCTION dbo.get_email_otp_by_criteria(
	email_param character varying,
	type_param character varying,
	minute_param integer,
	matched_param boolean)
    RETURNS TABLE(id integer, hashedotp character varying, email character varying, tried integer, type character varying, matched boolean, created_at timestamp without time zone) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT e.id, e.hashedotp, e.email, e.tried, e.type, e.matched, e.created_at
    FROM dbo.email_otp e
    WHERE
        e.email = email_param
        AND e.type = type_param
        AND e.tried = minute_param
        AND e.matched = matched_param;
END;
$BODY$;

ALTER FUNCTION dbo.get_email_otp_by_criteria(character varying, character varying, integer, boolean)
    OWNER TO postgres;


--- Insert email data --- 
CREATE OR REPLACE FUNCTION dbo.insert_email_data(
	hashed_otp_param character varying,
	email_param character varying,
	type_param character varying)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    -- Insert data into the 'dbo.email_otp' table
    INSERT INTO dbo.email_otp (hashedotp, email, type)
    VALUES (hashed_otp_param, email_param, type_param);
END;
$BODY$;

ALTER FUNCTION dbo.insert_email_data(character varying, character varying, character varying)
    OWNER TO postgres;



-- create log function

--- insert log ---
CREATE OR REPLACE FUNCTION dbo.insert_log(
	level character varying,
	message text)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    INSERT INTO dbo.app_logs (level, message, created_at) VALUES (level, message, CURRENT_TIMESTAMP);
END;
$BODY$;

ALTER FUNCTION dbo.insert_log(character varying, text)
    OWNER TO postgres;

--- log exception ---
CREATE OR REPLACE FUNCTION dbo.log_exception(
	stack_trace text,
	user_id integer,
	exception_message text,
	exception_type character varying)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    INSERT INTO dbo.exception_logs (stack_trace, user_id, exception_message, exception_type)
    VALUES (stack_trace, user_id, exception_message, exception_type);
END;
$BODY$;

ALTER FUNCTION dbo.log_exception(text, integer, text, character varying)
    OWNER TO postgres;

----------------------------------  Topics : Create vendor function , Author: Md. Iquball Hossain, Date: 22-11-2023 -------------------------------------

CREATE OR REPLACE FUNCTION vendors.insert_vendor(
    p_org_name VARCHAR,
    p_org_username VARCHAR,
    p_email VARCHAR,
    p_password_hash TEXT,
    p_phone_number VARCHAR,
    p_photo VARCHAR,
    p_address VARCHAR,
    p_city vendors.city_type,
    p_country vendors.country_type,
    p_business_category vendors.business_type,
    p_details VARCHAR,
    p_last_login_at TIMESTAMP WITHOUT TIME ZONE
) RETURNS VOID
LANGUAGE 'plpgsql'
COST 100
VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    INSERT INTO vendors.vendor (
        org_name, org_username, email, password_hash, phone_number, photo, 
        address, city, country, business_category, details, last_login_at
    ) VALUES (
        p_org_name, p_org_username, p_email, p_password_hash, p_phone_number,
        p_photo, p_address, p_city, p_country, p_business_category, p_details,
        p_last_login_at
    );
END;
$BODY$;

ALTER FUNCTION vendors.insert_vendor(
    VARCHAR, VARCHAR, VARCHAR, TEXT, VARCHAR, VARCHAR, VARCHAR, vendors.city_type, 
    vendors.country_type, vendors.business_type, VARCHAR, TIMESTAMP WITHOUT TIME ZONE
) OWNER TO postgres;

----------------------------------  Topics : Create notice for vendor by admin, Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------------------------

CREATE OR REPLACE FUNCTION admin.create_notice_for_vendor(
    vendor_identifier VARCHAR(255),
    notice_title VARCHAR(255),
    notice_topics TEXT,
    notice_file VARCHAR(255)
)
RETURNS VOID AS $$
BEGIN
    IF vendor_identifier ~ '^\d+$' THEN
        INSERT INTO admin.vendor_notice (vendor_id, notice_title, notice_topics, notice_file, notice_time)
        VALUES (CAST(vendor_identifier AS INT), notice_title, notice_topics, notice_file, current_timestamp);
    ELSE
        RAISE EXCEPTION 'Invalid vendor identifier: %', vendor_identifier;
    END IF;
END;
$$ LANGUAGE plpgsql;
ALTER FUNCTION admin.create_notice_for_vendor(
    VARCHAR,
    VARCHAR,
    TEXT,
    VARCHAR
) OWNER TO postgres;

----------------------------------  Topics : Edit notice for vendor by admin, Author: Md. Iquball Hossain, Date: 29-11-2023 -------------------------------------

DROP FUNCTION edit_notice_for_vendor(integer, character varying, text, character varying);

CREATE OR REPLACE FUNCTION edit_notice_for_vendor(
    notice_id INT,
    new_notice_title VARCHAR(255),
    new_notice_topics TEXT,
    new_notice_file VARCHAR(255)
)
RETURNS VOID AS $$
BEGIN
    UPDATE admin.vendor_notice
    SET notice_title = new_notice_title,
        notice_topics = new_notice_topics,
        notice_file = new_notice_file
    WHERE id = notice_id;
END;
$$ LANGUAGE plpgsql;

ALTER FUNCTION edit_notice_for_vendor(
    INT,
    VARCHAR(255),
    TEXT,
    VARCHAR(255)
) OWNER TO postgres;

----------------------------------  Topics : Delete notice for vendor by admin , Author: Md. Iquball Hossain, Date: 22-11-2023 -------------------------------------

CREATE OR REPLACE FUNCTION admin.delete_notice_for_vendor(
    notice_id INT
    )
RETURNS VOID AS $$
BEGIN
    DELETE FROM admin.vendor_notice WHERE id = notice_id;
END;
$$ LANGUAGE plpgsql;

ALTER FUNCTION admin.delete_notice_for_vendor(
    INT
) 
OWNER TO postgres;