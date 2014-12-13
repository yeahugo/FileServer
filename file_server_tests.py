import os
import shutil
import unittest
import tempfile
from nose.tools import raises

import file_server


class FileServerTest(unittest.TestCase):

    def setUp(self):
        file_server.app.config['REPO_PATH'] = tempfile.mkdtemp()
        file_server.app.config['TESTING'] = True
        self.app = file_server.app.test_client()

    def tearDown(self):
        shutil.rmtree(file_server.app.config['REPO_PATH'])

    def test_upload(self):
        rv = self.app.post('/upload/',
                           data={'upload': open('test/test.png', 'rb')})
        assert '.png' in rv.data
        assert 'test.png' not in rv.data

        path = os.path.join(file_server.app.config['REPO_PATH'], 'no-git-objects', 'te', 'test.png')
        assert not os.path.exists(path)

        path = os.path.join(file_server.app.config['REPO_PATH'], 'no-git-objects', 'links', 'te', 'test.png')
        assert not os.path.exists(path)

    def test_upload_with_name(self):
        rv = self.app.post('/upload/',
                           data={'name': 'test.png',
                                 'upload': open('test/test.png', 'rb')})
        assert '.png' in rv.data
        assert 'test.png' in rv.data

        path = os.path.join(file_server.app.config['REPO_PATH'], 'no-git-objects', 'te', 'test.png')
        assert not os.path.exists(path)

        path = os.path.join(file_server.app.config['REPO_PATH'], 'no-git-objects', 'links', 'te', 'test.png')
        assert os.path.exists(path)

    def test_upload_with_name_sha1(self):
        rv = self.app.post('/upload/',
                           data={'name': 'test.png', 'sha1': 1,
                                 'upload': open('test/test.png', 'rb')})
        assert '.png' in rv.data
        assert 'test.png' in rv.data

        path = os.path.join(file_server.app.config['REPO_PATH'], 'no-git-objects', 'te', 'test.png')
        assert os.path.exists(path)

        path = os.path.join(file_server.app.config['REPO_PATH'], 'no-git-objects', 'links', 'te', 'test.png')
        assert not os.path.exists(path)

    @raises(TypeError, IOError)
    def test_upload_show(self):
        rv = self.app.post('/upload/',
                           data={'upload': open('test/test.png', 'rb')},
                           follow_redirects=True)
        rv = self.app.get('/show/test.png/')
        assert rv.mimetype == 'image/png'
        assert rv.data == open('test/test.png', 'rb').read()

    def test_upload_with_name_show(self):
        rv = self.app.post('/upload/',
                           data={'name': 'test.png',
                                 'upload': open('test/test.png', 'rb')},
                           follow_redirects=True)
        rv = self.app.get('/show/test.png/')
        assert rv.mimetype == 'image/png'
        assert rv.data == open('test/test.png', 'rb').read()
