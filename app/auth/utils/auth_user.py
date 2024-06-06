# Preference Information
def user_preference_data(data):
    data = {
        "desired_gender": data.get("desired_gender"),
        "from_age": data.get("from_age"),
        "to_age": data.get("to_age"),
        "desired_country": data.get("desired_country"),
        "desired_community": data.get("desired_community"),
        "desired_occupation": data.get("desired_occupation"),
        "desired_education": data.get("desired_education"),
        "desired_language": data.get("desired_language"),
        "desired_religion": data.get("desired_religion"),
        "desired_marital_status": data.get("desired_marital_status"),
    }
    return data


# User Information
def user_information_data(data, photo):
    data = {
        "username": data.get("username"),
        "email": data.get("email"),
        "password_hash": data.get("password"),
        "phone_number": data.get("phone_number"),
        "photo": photo,
        "date_of_birth": data.get("date_of_birth"),
        "gender": data.get("gender"),
        "occupation": data.get("occupation"),
        "about_me": data.get("about_me"),
        "religion": data.get("religion"),
        "community": data.get("community"),
        "education": data.get("education"),
        "country": data.get("country"),
        "last_login_at": data.get("last_login_at")
    }
    return data
