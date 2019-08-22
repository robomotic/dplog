import unittest
from telemetry import Telemetry

class TestLocalTelemetry(unittest.TestCase):


    def setUp(self):
        pass

    @unittest.skip  # no reason needed
    def test_domain(self):
        tel = Telemetry()
        question = {'id': 1, 'title': 'telemetry test', 'observable': 'google.com', 'observable_type': 'D', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertGreater(count,0)

        question = {'id': 1, 'title': 'telemetry test', 'observable': 'stackexchange.com', 'observable_type': 'D', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertGreater(count, 0)

        question = {'id': 1, 'title': 'telemetry test', 'observable': 'github.com', 'observable_type': 'D', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertGreater(count, 0)

    @unittest.skip  # no reason needed
    def test_url(self):
        tel = Telemetry()
        question = {'id': 1, 'title': 'telemetry test', 'observable': 'https://stackoverflow.com/questions/11624190/python-convert-string-to-byte-array', 'observable_type': 'U', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertGreater(count, 0)

        question = {'id': 1, 'title': 'telemetry test', 'observable': 'https://www.gotomeet.me/auth/gateway', 'observable_type': 'U', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertGreater(count, 0)

        question = {'id': 1, 'title': 'telemetry test', 'observable': 'https://mail.google.com/mail/u/1/?pli=1', 'observable_type': 'U', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertGreater(count,0)

    def test_IP(self):
        tel = Telemetry()
        question = {'id': 1, 'title': 'telemetry test', 'observable': '127.0.0.1', 'observable_type': 'I', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertGreater(count, 0)

        question = {'id': 1, 'title': 'telemetry test', 'observable': '0.0.0.0', 'observable_type': 'I', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertEqual(count,0)

        question = {'id': 1, 'title': 'telemetry test', 'observable': '140.82.114.25', 'observable_type': 'I', 'begin_datetime': '2019-07-01T14:34:19Z', 'end_datetime': '2019-07-10T14:34:19Z', 'max_rounds': 1, 'algorithm': 'M', 'params': '{"p":0.1}', 'completed': False}

        (status,count) = tel.handle_observable(question)
        self.assertEqual(status,'OK')
        self.assertGreater(count,0)

if __name__ == '__main__':
    unittest.main()