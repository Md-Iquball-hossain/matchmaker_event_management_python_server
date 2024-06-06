# User Auth Data
# @Author Md Khairul Islam Ratul <khairul.m360ict@gmail.com>
# Date: 30-11-2023
from faker import Faker

fake = Faker()

# User Login Best Data
def user_login_best_data():
    return {
        "email": "khairul333@gmail.com",
        "password": "12345678"
    }

# User Login Wrong Data
def user_login_wrong_data():
    return {
        "email": fake.email(),
        "password": fake.password()
    }

# User Sign Up Best Data
def user_sign_up_best_data():
    data = {
        "username": f'rr{fake.user_name()}',
        "email":f'rr{fake.email()}',
        "password":fake.password(),
        "phone_number":fake.phone_number(),
        "date_of_birth":"2000-01-01",
        "religion":"muslim",
        "community":"Bengali",
        "country":"Bangladesh",
        "gender":fake.random_element(elements=('Male', 'Female')),
        "education":"B.E/B.Tech",
        "occupation":"Software Engineer",
        "about_me":"hello it's me."
    }
    # Create a temporary image file for upload
    file_name = f'{fake.first_name()}.jpg'
    with open(file_name, 'wb') as file:
        file.write(b'')  # You can replace this with actual file content

    files = {'photo': (file_name, open(file_name, 'rb'), 'image/jpeg')}

    return data, files

# User Sign Up Wrong Data
def user_sign_up_wrong_data():
    data = {
        "username":"khairul333",
        "email":"khairul333@gmail.com",
        "password":"12345678",
        "phone_number":"0170786357",
        "date_of_birth":"2000-01-01",
        "religion":"muslim",
        "community":"Bengali",
        "country":"Bangladesh",
        "gender":"Male",
        "education":"B.E/B.Tech",
        "occupation":"Software Engineer",
        "about_me":"hello it's me."
    }

    # Create a temporary image file for upload
    file_name = f'{fake.first_name()}.jpg'
    with open(file_name, 'wb') as file:
        file.write(b'')  # You can replace this with actual file content

    files = {'photo': (file_name, open(file_name, 'rb'), 'image/jpeg')}

    return data, files