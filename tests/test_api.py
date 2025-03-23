import sys
import os
import unittest
from io import BytesIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api import app


class TestFileUpload(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.upload_folder = self.app.config['UPLOAD_FOLDER']
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def tearDown(self):
        for filename in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def test_upload_file_success(self):
        test_file = BytesIO(b'Test file content')
        test_file.name = 'test.pdf'
        response = self.client.post('/upload', data={'file': (test_file, test_file.name)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "File uploaded successfully")
        self.assertTrue(os.path.exists(response.json['file_path']))

    def test_upload_no_file(self):
        response = self.client.post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "No file uploaded")

    def test_upload_unsupported_format(self):
        test_file = BytesIO(b'Test file content')
        test_file.name = 'test.txt'
        response = self.client.post('/upload', data={'file': (test_file, test_file.name)})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Unsupported file format. Only PDF and PPTX files are allowed")

    def test_upload_empty_file(self):
        test_file = BytesIO(b'')
        test_file.name = 'empty.pdf'
        response = self.client.post('/upload', data={'file': (test_file, test_file.name)})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "File is empty")

    def test_upload_file_overwrite(self):
        test_file = BytesIO(b'Test file content')
        test_file.name = 'test.pdf'
        self.client.post('/upload', data={'file': (test_file, test_file.name)})
        test_file.seek(0)
        response = self.client.post('/upload', data={'file': (test_file, test_file.name)})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "A file with this name already exists")

    def test_upload_file_size_exceeded(self):
        test_file = BytesIO(os.urandom(11 * 1024 * 1024))  # 11MB file
        test_file.name = 'large.pdf'
        response = self.client.post('/upload', data={'file': (test_file, test_file.name)})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "File size exceeds the 10MB limit")

    def test_upload_file_save_error(self):
        os.chmod(self.upload_folder, 0o444)
        test_file = BytesIO(b'Test file content')
        test_file.name = 'test.pdf'
        response = self.client.post('/upload', data={'file': (test_file, test_file.name)})
        self.assertEqual(response.status_code, 500)
        self.assertIn("Failed to save file", response.json['error'])
        os.chmod(self.upload_folder, 0o755)

if __name__ == '__main__':
    unittest.main()
