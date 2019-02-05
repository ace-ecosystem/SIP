from project.tests.helpers import *

"""
CREATE TESTS
"""


def test_create_schema(client):
    """ Ensure POST requests conform to the required JSON schema """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    # Invalid JSON
    data = {}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['msg'] == 'Request must include valid JSON'

    # Missing required email parameter
    data = {'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['msg'] == "Request JSON does not match schema: 'email' is a required property"

    # Missing required first_name parameter
    data = {'email': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['msg'] == "Request JSON does not match schema: 'first_name' is a required property"

    # Missing required last_name parameter
    data = {'first_name': 'asdf', 'email': 'asdf', 'password': 'asdf', 'roles': ['asdf'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['msg'] == "Request JSON does not match schema: 'last_name' is a required property"

    # Missing required password parameter
    data = {'first_name': 'asdf', 'last_name': 'asdf', 'email': 'asdf', 'roles': ['asdf'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['msg'] == "Request JSON does not match schema: 'password' is a required property"

    # Missing required roles parameter
    data = {'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'email': 'asdf', 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['msg'] == "Request JSON does not match schema: 'roles' is a required property"

    # Missing required username parameter
    data = {'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'], 'email': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['msg'] == "Request JSON does not match schema: 'username' is a required property"

    # Additional parameter
    data = {'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'], 'email': 'asdf',
            'username': 'asdf', 'asdf': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'Additional properties are not allowed' in response['msg']

    # Invalid email parameter type
    data = {'email': 1, 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # email parameter too short
    data = {'email': '', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # email parameter too long
    data = {'email': 'a' * 256, 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']

    # Invalid first_name parameter type
    data = {'email': 'asdf', 'first_name': 1, 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # first_name parameter too short
    data = {'email': 'asdf', 'first_name': '', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # first_name parameter too long
    data = {'email': 'asdf', 'first_name': 'a' * 51, 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']

    # Invalid last_name parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 1, 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # last_name parameter too short
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': '', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # last_name parameter too long
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'a' * 51, 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']

    # Invalid password parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 1, 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # password parameter too short
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': '', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # Invalid roles parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': 'asdf',
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "'asdf' is not of type 'array'" in response['msg']

    # Invalid roles parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': 1,
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'array'" in response['msg']

    # Empty roles parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': [],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # roles parameter too short
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': [''],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # roles parameter too long
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['a' * 81],
            'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']

    # Invalid username parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 1}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # username parameter too short
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': ''}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # username parameter too long
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'a' * 256}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']


def test_create_duplicate(client):
    """ Ensure a duplicate record cannot be created """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf',
            'password': 'asdf', 'roles': ['analyst'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    assert request.status_code == 201

    # Try making a duplicate email
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf',
            'password': 'asdf', 'roles': ['analyst'], 'username': 'asdf2'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['msg'] == 'User email already exists'

    # Try making a duplicate username
    data = {'email': 'asdf2', 'first_name': 'asdf', 'last_name': 'asdf',
            'password': 'asdf', 'roles': ['analyst'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['msg'] == 'User username already exists'


def test_create_missing_token(app, client):
    """ Ensure a token is given if the config requires it """

    app.config['POST'] = 'admin'

    request = client.post('/api/users')
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['msg'] == 'Missing Authorization Header'


def test_create_invalid_role(app, client):
    """ Ensure the given token has the proper role access """

    app.config['POST'] = 'admin'

    access_token, refresh_token = obtain_token(client, 'analyst', 'analyst')
    headers = create_auth_header(access_token)
    request = client.post('/api/users', headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['msg'] == 'admin role required'


def test_create(client):
    """ Ensure a proper request actually works """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    # Try with a roles list
    data = {'email': 'asdf2', 'first_name': 'asdf', 'last_name': 'asdf',
            'password': 'asdf', 'roles': ['analyst', 'admin'], 'username': 'asdf2'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 201
    assert response['roles'] == ['admin', 'analyst']
    assert response['username'] == 'asdf2'


"""
READ TESTS
"""


def test_read_nonexistent_id(client):
    """ Ensure a nonexistent ID does not work """

    request = client.get('/api/users/100000')
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['msg'] == 'User ID not found'


def test_read_missing_token(app, client):
    """ Ensure a token is given if the config requires it """

    app.config['GET'] = 'admin'

    request = client.get('/api/users/1')
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['msg'] == 'Missing Authorization Header'


def test_read_invalid_role(app, client):
    """ Ensure the given token has the proper role access """

    app.config['GET'] = 'admin'

    access_token, refresh_token = obtain_token(client, 'analyst', 'analyst')
    headers = create_auth_header(access_token)
    request = client.get('/api/users/1', headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['msg'] == 'admin role required'


def test_read_all_values(client):
    """ Ensure all values properly return """

    request = client.get('/api/users')
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert len(response) == 3


def test_read_by_id(client):
    """ Ensure names can be read by their ID """

    request = client.get('/api/users/1')
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response['id'] == 1
    assert 'apikey' not in response


"""
UPDATE TESTS
"""


def test_update_schema(client):
    """ Ensure PUT requests conform to the required JSON schema """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    # Invalid JSON
    data = {}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['msg'] == 'Request must include valid JSON'

    # Additional parameter
    data = {'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'], 'email': 'asdf',
            'username': 'asdf', 'asdf': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'Additional properties are not allowed' in response['msg']

    # Invalid email parameter type
    data = {'email': 1, 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # email parameter too short
    data = {'email': '', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # email parameter too long
    data = {'email': 'a' * 256, 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']

    # Invalid first_name parameter type
    data = {'email': 'asdf', 'first_name': 1, 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # first_name parameter too short
    data = {'email': 'asdf', 'first_name': '', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # first_name parameter too long
    data = {'email': 'asdf', 'first_name': 'a' * 51, 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']

    # Invalid last_name parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 1, 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # last_name parameter too short
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': '', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # last_name parameter too long
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'a' * 51, 'password': 'asdf', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']

    # Invalid password parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 1, 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # password parameter too short
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': '', 'roles': ['asdf'],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # Invalid roles parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': 'asdf',
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "'asdf' is not of type 'array'" in response['msg']

    # Invalid roles parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': 1,
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'array'" in response['msg']

    # Empty roles parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': [],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # roles parameter too short
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': [''],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # roles parameter too long
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['a' * 81],
            'username': 'asdf'}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']

    # Invalid username parameter type
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 1}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "1 is not of type 'string'" in response['msg']

    # username parameter too short
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': ''}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too short' in response['msg']

    # username parameter too long
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf', 'password': 'asdf', 'roles': ['asdf'],
            'username': 'a' * 256}
    request = client.put('/api/users/1', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert 'too long' in response['msg']


def test_update_nonexistent_id(client):
    """ Ensure a nonexistent ID does not work """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf',
            'password': 'asdf', 'roles': ['analyst', 'admin'], 'username': 'asdf'}
    request = client.put('/api/users/100000', json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['msg'] == 'User ID not found'


def test_update_duplicate(client):
    """ Ensure duplicate records cannot be updated """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf',
            'password': 'asdf', 'roles': ['analyst'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201
    assert response['roles'] == ['analyst']
    assert response['username'] == 'asdf'

    # Try to update an existing email
    data = {'email': 'asdf'}
    request = client.put('/api/users/{}'.format(_id), json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['msg'] == 'User email already exists'

    # Try to update an existing username
    data = {'username': 'asdf'}
    request = client.put('/api/users/{}'.format(_id), json=data, headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['msg'] == 'User username already exists'


def test_update_missing_token(app, client):
    """ Ensure a token is given if the config requires it """

    app.config['PUT'] = 'admin'

    request = client.put('/api/users/1')
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['msg'] == 'Missing Authorization Header'


def test_update_invalid_role(app, client):
    """ Ensure the given token has the proper role access """

    app.config['PUT'] = 'admin'

    access_token, refresh_token = obtain_token(client, 'analyst', 'analyst')
    headers = create_auth_header(access_token)
    request = client.put('/api/users/1', headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['msg'] == 'admin role required'


def test_update(client):
    """ Ensure a proper request actually works """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)
    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf',
            'password': 'asdf', 'roles': ['analyst', 'admin'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201
    assert response['active'] is True
    assert response['roles'] == ['admin', 'analyst']

    # Update active
    data = {'active': False}
    request = client.put('/api/users/{}'.format(_id), json=data, headers=headers)
    assert request.status_code == 200

    request = client.get('/api/users/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response['id'] == _id
    assert response['active'] is False

    # Update email
    data = {'email': 'asdf2'}
    request = client.put('/api/users/{}'.format(_id), json=data, headers=headers)
    assert request.status_code == 200

    request = client.get('/api/users/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response['id'] == _id
    assert response['email'] == 'asdf2'

    # Update first_name
    data = {'first_name': 'asdf2'}
    request = client.put('/api/users/{}'.format(_id), json=data, headers=headers)
    assert request.status_code == 200

    request = client.get('/api/users/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response['id'] == _id
    assert response['first_name'] == 'asdf2'

    # Update last_name
    data = {'last_name': 'asdf2'}
    request = client.put('/api/users/{}'.format(_id), json=data, headers=headers)
    assert request.status_code == 200

    request = client.get('/api/users/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response['id'] == _id
    assert response['last_name'] == 'asdf2'

    # Password
    # TODO: Not sure how to effectively test changing password.

    # Update roles with a list
    data = {'roles': ['analyst', 'admin']}
    request = client.put('/api/users/{}'.format(_id), json=data, headers=headers)
    assert request.status_code == 200

    request = client.get('/api/users/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response['id'] == _id
    assert response['roles'] == ['admin', 'analyst']


"""
DELETE TESTS
"""


def test_delete_nonexistent_id(client):
    """ Ensure a nonexistent ID does not work """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)
    request = client.delete('/api/users/100000', headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['msg'] == 'User ID not found'


def test_delete_missing_token(app, client):
    """ Ensure a token is given if the config requires it """

    app.config['DELETE'] = 'admin'

    request = client.delete('/api/users/1')
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['msg'] == 'Missing Authorization Header'


def test_delete_invalid_role(app, client):
    """ Ensure the given token has the proper role access """

    app.config['DELETE'] = 'admin'

    access_token, refresh_token = obtain_token(client, 'analyst', 'analyst')
    headers = create_auth_header(access_token)
    request = client.delete('/api/users/1', headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['msg'] == 'admin role required'


def test_delete_foreign_key_event(client):
    """ Ensure you cannot delete with foreign key constraints """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    user_request, user_response = create_user(client, 'asdf@asdf.com', 'asdf', 'asdf', 'asdf', ['analyst'], 'some_guy')
    event_request, event_response = create_event(client, 'test_event', 'some_guy')
    assert user_request.status_code == 201
    assert event_request.status_code == 201

    request = client.delete('/api/users/{}'.format(user_response['id']), headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['msg'] == 'Unable to delete user due to foreign key constraints'


def test_delete_foreign_key_indicator(client):
    """ Ensure you cannot delete with foreign key constraints """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    user_request, user_response = create_user(client, 'asdf@asdf.com', 'asdf', 'asdf', 'asdf', ['analyst'], 'some_guy')
    indicator_request, indicator_response = create_indicator(client, 'IP', '127.0.0.1', 'some_guy')
    assert user_request.status_code == 201
    assert indicator_request.status_code == 201

    request = client.delete('/api/users/{}'.format(user_response['id']), headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['msg'] == 'Unable to delete user due to foreign key constraints'


def test_delete_foreign_key_reference(client):
    """ Ensure you cannot delete with foreign key constraints """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    user_request, user_response = create_user(client, 'asdf@asdf.com', 'asdf', 'asdf', 'asdf', ['analyst'], 'some_guy')
    reference_request, reference_response = create_intel_reference(client, 'some_guy', 'OSINT', 'http://blahblah.com')
    assert user_request.status_code == 201
    assert reference_request.status_code == 201

    request = client.delete('/api/users/{}'.format(user_response['id']), headers=headers)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['msg'] == 'Unable to delete user due to foreign key constraints'


def test_delete(client):
    """ Ensure a proper request actually works """

    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    data = {'email': 'asdf', 'first_name': 'asdf', 'last_name': 'asdf',
            'password': 'asdf', 'roles': ['analyst', 'admin'], 'username': 'asdf'}
    request = client.post('/api/users', json=data, headers=headers)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201

    request = client.delete('/api/users/{}'.format(_id), headers=headers)
    assert request.status_code == 204

    request = client.get('/api/users/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['msg'] == 'User ID not found'
