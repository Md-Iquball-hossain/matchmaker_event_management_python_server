

def match_score(user_profile, user_preference):
    print("user_profile", user_profile)
    print("user_preference", user_preference)
    # Calculate a match score based on user preferences
    score = 0

    # Age match: Higher weight for age within the desired range
    if user_preference.from_age <= user_profile.age <= user_preference.to_age:
        score += 20  # Adjust the weight as needed

    # Other preference matches: Add to the score for each matching preference
    if user_profile.religion == user_preference.desired_religion:
        score += 10
    if user_profile.country == user_preference.desired_country:
        score += 10
    if user_profile.community == user_preference.desired_community:
        score += 10
    if user_profile.occupation == user_preference.desired_occupation:
        score += 10
    if user_profile.education == user_preference.desired_education:
        score += 10
    if user_profile.language == user_preference.desired_language:
        score += 10
    if user_profile.gender == user_preference.desired_gender:
        score += 10

    return score
