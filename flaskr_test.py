import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fb, flaskr.DATABSE = tempfile.mkstemp()
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fb)
        os.unlink(flaskr.DATABSE)

    def test_empty_db(self):
        res = self.app.get('/')
        assert 'No entries here so far'.encode('utf-8') in res.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        res = self.login('admin', 'default')
        assert b'You were logged in' in res.data
        res = self.logout()
        assert b'You were logged out' in res.data
        res = self.login('adminx', 'default')
        assert b'Invalid username' in res.data
        res = self.login('admin', 'defaultx')
        assert b'Invalid password' in res.data

    def test_messages(self):
        self.login('admin', 'default')
        res = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in res.data
        assert b'&lt;Hello&gt' in res.data
        assert b'<strong>HTML</strong> allowed here' in res.data

if __name__ == '__main__':
    unittest.main()
