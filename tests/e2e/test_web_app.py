import pytest

from flask import session


def test_register(client):
    # check if we get register page
    response_code = client.get('/auth/register').status_code
    assert response_code == 200

    # check that when supplied with a valid user name and password, user is registered successfully
    response = client.post(
        '/auth/register',
        data={'user_name': 'tim', 'password': 'dharmanvideoS1'}
    )
    assert response.headers['Location'] == '/auth/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('bo', '', b'Your username is too short!'),
        ('jewel', '', b'Your password is required'),
        ('jewel', 'test', b'Password must be at least 8 characters long, contain at least one number, one uppercase letter and one lowercase letter'),
        ('fmercury', 'Test#6^0', b'That username is taken, please choose another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    client.post(
        '/auth/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^01'}
    )

    response = client.post(
        '/auth/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data
    # i cry


def test_login(client, auth):
    # check can retrive login page
    status_code = client.get('/auth/login').status_code
    assert status_code == 200

    # register
    auth.register(user_name='thorke', password='Pass1234')

    # check if success login redirects to home page
    response = auth.login(user_name='thorke', password='Pass1234')
    assert response.headers['Location'] == '/'

    # check session is created for logged in user
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    auth.register(user_name='thorke', password='Pass1234')

    auth.login(user_name='thorke', password='Pass1234')

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session

def test_home_non_logged_in_user(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome,' in response.data

def test_home_logged_in_user(client, auth):
    # initialise user
    auth.register(user_name='thorke', password='Pass1234')
    auth.login(user_name='thorke', password='Pass1234')

    # Check that we can retrieve the home page.

    with client:
        response = client.get('/')
        assert response.status_code == 200
        assert session['user_name'] == 'thorke'
        assert b'Welcome Thorke,' in response.data

def test_non_logged_in_cannot_access_user_page(client):
    response = client.get('/user/thorke')
    # non-logged in user tries to access a user page, will be redirected
    assert response.status_code == 302



def test_logged_in_user_can_access_user_page(client, auth):
    # initialise user
    auth.register(user_name='thorke', password='Pass1234')
    auth.login(user_name='thorke', password='Pass1234')

    response = client.get('/user/thorke')
    # user page is not found, register page replaces user page
    assert response.status_code == 200


def test_non_logged_in_user_cannot_make_review(client):
    response = client.post('/browse/4')
    assert response.status_code == 400



def test_logged_in_user_can_make_review(client, auth):
    # initialise user
    auth.register(user_name='thorke', password='Pass1234')
    auth.login(user_name='thorke', password='Pass1234')


    response = client.get('/browse/5')
    assert response.status_code == 200
    response = client.post(
        '/browse/5',
        data={'review': 'Not bad', 'rating': 5}
    )
    assert response.status_code == 302

    response = client.get('/browse/5')
    assert b'Not bad' in response.data

@pytest.mark.parametrize(('review', 'rating', 'messages'), (
                         ('ass', 5, (b'Comment must be at least 4 characters long.', b'Your comment must not contain profanity.')),
                         ('Garabagio! fuck this song', 3, (b'Your comment must not contain profanity.')),
                         ('Hey', 1, (b'Comment must be at least 4 characters long.'))

                         ))
def test_comment_with_invalid_input(client, auth, review, rating, messages):
    # initialise user
    auth.register(user_name='thorke', password='Pass1234')
    auth.login(user_name='thorke', password='Pass1234')

    # get a track to comment on
    client.get('/browse/5')

    # attempt to review
    response = client.post(
        '/browse/5',
        data={'review': review, 'rating': rating}
    )

    for message in messages:
        assert message in response.data


def test_search_page_can_view_release_years(client):
    # get search page and view release years
    response = client.get('/search?view_target=Release+Years')
    assert response.status_code == 200
    assert b'1981' in response.data

def test_search_page_can_view_artists(client):
    # get search page and view artists
    response = client.get('/search?view_target=Artists')
    assert response.status_code == 200
    assert b'??ss' in response.data

def test_search_page_can_view_albums(client):
    # get search page and view albums
    response = client.get('/search?view_target=Albums')
    assert response.status_code == 200
    assert b'4: All Aboard the Magic Pus' in response.data

def test_search_page_can_view_genres(client):
    # get search page and view genres
    response = client.get('/search?view_target=Genres')
    assert response.status_code == 200
    assert b'African' in response.data


def test_can_get_tracks_by_date(client):
    # get search page
    response = client.get('/search')
    assert response.status_code == 200

    response = client.post(
        '/search',
        data={'search': 2000, 'search_type': 'release year'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/search_by_date?target_date=2000'

def test_does_not_get_tracks_by_non_existent_date(client):

    response = client.get('/search_by_date?target_date=2010')
    assert response.headers['Location'] == '/not_found?target_search=2010&term=Release+Year'

    # redirects to not found page, check message
    response = client.get('/not_found?target_search=2010&term=Release+Year')
    assert b'No Release Year results for \'2010\'' in response.data

def test_can_get_tracks_by_album(client):
    # get search page
    status_code = client.get('/search').status_code
    assert status_code == 200

    response = client.post(
        '/search',
        data={'search': 'The', 'search_type': 'album'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/search_by_album?target_album=The'


def test_does_not_get_tracks_by_non_existent_album(client):

    response = client.get('/search_by_album?target_album=Non+existent')
    assert response.headers['Location'] == '/not_found?target_search=Non+existent&term=Album'

    # redirects to not found page, check message
    response = client.get('/not_found?target_search=Non+existent&term=Album')
    assert b'No Album results for \'Non existent\'' in response.data

def test_can_get_tracks_by_artist(client):
    # get search page
    status_code = client.get('/search').status_code
    assert status_code == 200

    response = client.post(
        '/search',
        data={'search': 'Br', 'search_type': 'artist'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/search_by_artist?target_artist=Br'


def test_does_not_get_tracks_by_non_existent_artist(client):

    response = client.get('/search_by_artist?target_artist=Bruce')
    assert response.headers['Location'] == '/not_found?target_search=Bruce&term=Artist'

    # redirects to not found page, check message
    response = client.get('/not_found?target_search=Bruce&term=Artist')
    assert b'No Artist results for \'Bruce\'' in response.data


def test_can_get_tracks_by_genre(client):
    # get search page
    status_code = client.get('/search').status_code
    assert status_code == 200

    response = client.post(
        '/search',
        data={'search': 'ex', 'search_type': 'genre'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/search_by_genre?target_genre=ex'


def test_does_not_get_tracks_by_non_existent_genre(client):

    response = client.get('/search_by_genre?target_genre=Grunge')
    assert response.headers['Location'] == '/not_found?target_search=Grunge&term=Genre'

    # redirects to not found page, check message
    response = client.get('/not_found?target_search=Grunge&term=Genre')
    assert b'No Genre results for \'Grunge\'' in response.data


def test_can_get_tracks_by_track_title(client):
    # get search page
    status_code = client.get('/search').status_code
    assert status_code == 200

    response = client.post(
        '/search',
        data={'search': 'Sun', 'search_type': 'track'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/search_by_track?target_track=Sun'


def test_does_not_get_tracks_by_non_existent_track_title(client):

    response = client.get('/search_by_track?target_track=Sunscreen')
    assert response.headers['Location'] == '/not_found?target_search=Sunscreen&term=Track+Title'

    # redirects to not found page, check message
    response = client.get('/not_found?target_search=Sunscreen&term=Track+Title')
    assert b'No Track Title results for \'Sunscreen\'' in response.data