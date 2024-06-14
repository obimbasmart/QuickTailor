


def test_new_user(new_user):
    """
    given: a User model
    when: a new User is created
    then: check the email, hashed_password, and role fields are defined correctly
    """
    assert new_user.email == 'olegbyonic@gmail.com'
    assert new_user.first_name == 'oleg'
    assert new_user.last_name ==  'byonic'
    assert new_user.is_tailor == False
    assert new_user.password_hash != 'very_strong_pwd'
    