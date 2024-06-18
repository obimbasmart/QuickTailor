"""
    unit tests for app authentication views
"""

def test_home_page(client):
    """
    @when: the '/' page is requested (GET)
    @then: check that the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Discover" in response.data
    assert b"Login" in response.data


def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"Mission" in response.data


def test_register(client):
    """test the registeration page"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b"as Tailor" in response.data
    assert b"as User" in response.data

    response = client.get('/register/not_good')
    assert response.status_code == 404


def test_hiw_page(client):
    """test the how_it_works page"""
    response = client.get('/how-it-works')
    assert response.status_code == 200
    assert b"Enjoy" in response.data


def test_cart_page_logged_out(client):
    """test that /cart redirects to /login for logged out user"""
    response = client.get('/cart')
    assert response.status_code == 302