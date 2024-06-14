"""
    unit tests for app authentication views
"""

from app.models.user import User

def test_register_user(client, new_user: User, _db):
    """
        @when: /register/user is requested (POST)
        @then: test that response is valid
    """
    res = client.get('register/user')
    assert res.status_code == 200

    res = client.post('/register/user', data={
        'first_name': new_user.first_name,
        'email': new_user.email,
        'phone_number': new_user.phone_no,
        'password': new_user.password
    }, follow_redirects=True)

    assert res.status_code == 200
    user = _db.session.query(User).one_or_404()
    
    assert user.password_hash != new_user.password
    assert user.first_name == new_user.first_name

    # TODO: last name should be from form data not 'good name'
    assert user.last_name ==  'good name'
    assert user.phone_no == new_user.phone_no
    assert user.email == new_user.email

    assert user.is_tailor == False
    assert b'Login' in res.data

def test_login(new_user: User, client, _db):
    response = client.post('/login', data={
        'email': new_user.email,
        'password': new_user.password
    }, follow_redirects=True)

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert '_user_id' in session

def test_logout(client):
    res = client.post('/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b"Discover" in res.data

    with client.session_transaction() as session:
        assert '_user_id' not in session