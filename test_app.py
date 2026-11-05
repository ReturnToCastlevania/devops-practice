import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from app import Handler

class ServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def test_health(self):
        conn = HTTPConnection('127.0.0.1', self.server.server_port, timeout=2)
        try:
            conn.request('GET', '/healthz')
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read()), {'status': 'ok'})
        finally:
            conn.close()


    def test_missing(self):
        conn = HTTPConnection('127.0.0.1', self.server.server_port, timeout=2)
        try:
            conn.request('GET', '/missing')
            response = conn.getresponse()
            self.assertEqual(response.status, 404)
            self.assertEqual(json.loads(response.read()), {'error': 'not found'})
        finally:
            conn.close()

if __name__ == '__main__':
    unittest.main()

