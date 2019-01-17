import json

from flask import current_app

from project.tests.base import BaseTestCase
from project.tests.base import TEST_ADMIN_APIKEY, TEST_ANALYST_APIKEY, TEST_INVALID_APIKEY


class TestCampaignAlias(BaseTestCase):
    """ Tests for the Campaign Alias API calls """

    """
    CREATE TESTS
    """

    def test_create_missing_parameter(self):
        """ Ensure the required parameters are given """

        with self.client:
            current_app.config['POST'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 400)
            self.assertEqual(response['message'], 'Request must include: alias, campaign')

            data = {'apikey': TEST_ANALYST_APIKEY, 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 400)
            self.assertEqual(response['message'], 'Request must include: alias, campaign')

    def test_create_duplicate_alias(self):
        """ Ensure duplicate alias cannot be created """

        with self.client:
            current_app.config['POST'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'name': 'asdf'}
            request = self.client.post('/api/campaigns', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 409)
            self.assertEqual(response['message'], 'Campaign alias already exists')

    def test_create_missing_api_key(self):
        """ Ensure an API key is given if the config requires it """

        with self.client:
            current_app.config['POST'] = 'analyst'

            data = {'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'Bad or missing API key')

    def test_create_invalid_api_key(self):
        """ Ensure an API key not found in the database does not work """

        with self.client:
            current_app.config['POST'] = 'analyst'

            data = {'apikey': TEST_INVALID_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'API user does not exist')

    def test_create_invalid_role(self):
        """ Ensure the given API key has the proper role access """

        with self.client:
            current_app.config['POST'] = 'user_does_not_have_this_role'

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'Insufficient privileges')

    def test_create(self):
        """ Ensure a proper request actually works """

        with self.client:
            current_app.config['POST'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'name': 'asdf'}
            request = self.client.post('/api/campaigns', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

    """
    READ TESTS
    """

    def test_read_nonexistent_id(self):
        """ Ensure a nonexistent ID does not work """

        with self.client:
            current_app.config['GET'] = None

            request = self.client.get('/api/campaigns/alias/100')
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 404)
            self.assertEqual(response['message'], 'Campaign alias ID not found')

    def test_read_missing_api_key(self):
        """ Ensure an API key is given if the config requires it """

        with self.client:
            current_app.config['GET'] = 'analyst'

            request = self.client.get('/api/campaigns/alias/1')
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'Bad or missing API key')

    def test_read_invalid_api_key(self):
        """ Ensure an API key not found in the database does not work """

        with self.client:
            current_app.config['GET'] = 'analyst'

            request = self.client.get('/api/campaigns/alias/1?apikey={}'.format(TEST_INVALID_APIKEY))
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'API user does not exist')

    def test_read_invalid_role(self):
        """ Ensure the given API key has the proper role access """

        with self.client:
            current_app.config['GET'] = 'user_does_not_have_this_role'

            request = self.client.get('/api/campaigns/alias/1?apikey={}'.format(TEST_ANALYST_APIKEY))
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'Insufficient privileges')

    def test_read_all_aliases(self):
        """ Ensure all aliases properly return """

        with self.client:
            current_app.config['GET'] = None
            current_app.config['POST'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'name': 'asdf'}
            request = self.client.post('/api/campaigns', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf2', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf3', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

            request = self.client.get('/api/campaigns/alias')
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 200)
            self.assertEqual(len(response), 3)

    def test_read_by_id(self):
        """ Ensure aliases can be read by their ID """

        with self.client:
            current_app.config['GET'] = None
            current_app.config['POST'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'name': 'asdf'}
            request = self.client.post('/api/campaigns', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

            request = self.client.get('/api/campaigns/alias/1')
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 200)
            self.assertEqual(response['id'], 1)
            self.assertEqual(response['alias'], 'asdf')
            self.assertEqual(response['campaign'], 'asdf')

    """
    UPDATE TESTS
    """

    def test_update_nonexistent_id(self):
        """ Ensure a nonexistent ID does not work """

        with self.client:
            current_app.config['PUT'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.put('/api/campaigns/alias/100', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 404)
            self.assertEqual(response['message'], 'Campaign alias ID not found')

    def test_update_duplicate_value(self):
        """ Ensure duplicate aliases cannot be updated """

        with self.client:
            current_app.config['POST'] = 'analyst'
            current_app.config['PUT'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'name': 'asdf'}
            request = self.client.post('/api/campaigns', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.put('/api/campaigns/alias/1', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 409)
            self.assertIn(response['message'], 'Campaign alias already exists')

    def test_update_missing_api_key(self):
        """ Ensure an API key is given if the config requires it """

        with self.client:
            current_app.config['PUT'] = 'analyst'

            data = {'alias': 'asdf'}
            request = self.client.put('/api/campaigns/alias/1', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'Bad or missing API key')

    def test_update_invalid_api_key(self):
        """ Ensure an API key not found in the database does not work """

        with self.client:
            current_app.config['PUT'] = 'analyst'

            data = {'apikey': TEST_INVALID_APIKEY, 'alias': 'asdf'}
            request = self.client.put('/api/campaigns/alias/1', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'API user does not exist')

    def test_update_invalid_role(self):
        """ Ensure the given API key has the proper role access """

        with self.client:
            current_app.config['PUT'] = 'user_does_not_have_this_role'

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf'}
            request = self.client.put('/api/campaigns/alias/1', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'Insufficient privileges')

    def test_update(self):
        """ Ensure a proper request actually works """

        with self.client:
            current_app.config['GET'] = None
            current_app.config['POST'] = 'analyst'
            current_app.config['PUT'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'name': 'asdf'}
            request = self.client.post('/api/campaigns', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'name': 'asdf2'}
            request = self.client.post('/api/campaigns', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf2', 'campaign': 'asdf2'}
            request = self.client.put('/api/campaigns/alias/1', data=data)
            self.assertEqual(request.status_code, 200)

            request = self.client.get('/api/campaigns/alias/1')
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 200)
            self.assertEqual(response['id'], 1)
            self.assertEqual(response['alias'], 'asdf2')
            self.assertEqual(response['campaign'], 'asdf2')

    """
    DELETE TESTS
    """

    def test_delete_nonexistent_id(self):
        """ Ensure a nonexistent ID does not work """

        with self.client:
            current_app.config['DELETE'] = 'admin'

            data = {'apikey': TEST_ADMIN_APIKEY}
            request = self.client.delete('/api/campaigns/alias/100', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 404)
            self.assertEqual(response['message'], 'Campaign alias ID not found')

    def test_delete_missing_api_key(self):
        """ Ensure an API key is given if the config requires it """

        with self.client:
            current_app.config['DELETE'] = 'admin'

            request = self.client.delete('/api/campaigns/alias/100')
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'Bad or missing API key')

    def test_delete_invalid_api_key(self):
        """ Ensure an API key not found in the database does not work """

        with self.client:
            current_app.config['DELETE'] = 'admin'

            data = {'apikey': TEST_INVALID_APIKEY}
            request = self.client.delete('/api/campaigns/alias/1', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'API user does not exist')

    def test_delete_invalid_role(self):
        """ Ensure the given API key has the proper role access """

        with self.client:
            current_app.config['DELETE'] = 'user_does_not_have_this_role'

            data = {'apikey': TEST_ANALYST_APIKEY}
            request = self.client.delete('/api/campaigns/alias/1', data=data)
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 401)
            self.assertEqual(response['message'], 'Insufficient privileges')

    def test_delete(self):
        """ Ensure a proper request actually works """

        with self.client:
            current_app.config['DELETE'] = 'admin'
            current_app.config['GET'] = None
            current_app.config['POST'] = 'analyst'

            data = {'apikey': TEST_ANALYST_APIKEY, 'name': 'asdf'}
            request = self.client.post('/api/campaigns', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ANALYST_APIKEY, 'alias': 'asdf', 'campaign': 'asdf'}
            request = self.client.post('/api/campaigns/alias', data=data)
            self.assertEqual(request.status_code, 201)

            data = {'apikey': TEST_ADMIN_APIKEY}
            request = self.client.delete('/api/campaigns/alias/1', data=data)
            self.assertEqual(request.status_code, 204)

            request = self.client.get('/api/campaigns/alias/1')
            response = json.loads(request.data.decode())
            self.assertEqual(request.status_code, 404)
            self.assertEqual(response['message'], 'Campaign alias ID not found')