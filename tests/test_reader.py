#!/usr/bin/env python
import unittest
import os
import sys

from impulsare_config import Reader, utils

base_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, base_path + '/../')


# https://docs.python.org/3/library/unittest.html#assert-methods
class TestReader(unittest.TestCase):
    def test_default(self):
        if os.path.isfile(utils.get_venv_basedir() + '/config/app.yml'):
            return

        with self.assertRaisesRegex(IOError, 'Missing config file: "(.+)config/app\.yml" does not exist'):
            Reader().parse()

    def test_overriden(self):
        with self.assertRaisesRegex(IOError, 'Missing config file: "/does/not/exist" does not exist'):
            Reader().parse('/does/not/exist')


    def test_exists(self):
        cf = Reader()
        self.assertIs(type(cf), Reader)


    def test_valid_config(self):
        config_file = base_path + '/static/config_valid.yml'
        specs_file = base_path + '/static/specs.yml'

        cf = Reader()
        config_data = cf.parse(config_file, specs_file)
        self.assertIsInstance(config_data, dict)

        self.assertIn('debug', config_data)
        self.assertTrue(config_data['debug'])

        self.assertIn('logger', config_data)
        self.assertEqual('syslog', config_data['logger'])


    def test_valid_config_bad_default(self):
        config_file = base_path + '/static/config_empty.yml'
        specs_file = base_path + '/static/specs.yml'

        with self.assertRaisesRegex(IOError, 'Your default .+ does not exist'):
            Reader().parse(config_file=config_file, specs=specs_file, default_file='/does/not/exists')


    def test_valid_config_bad_specs(self):
        config_file = base_path + '/static/config_empty.yml'

        with self.assertRaisesRegex(IOError, 'Your specs .+ does not exist'):
            Reader().parse(config_file=config_file, specs='/does/not/exists')


    def test_empty_config(self):
        config_file = base_path + '/static/config_empty.yml'
        specs_file = base_path + '/static/specs.yml'
        default_config_file = base_path + '/static/default.yml'

        cf = Reader()
        config_data = cf.parse(config_file, specs_file, default_config_file)
        self.assertIsInstance(config_data, dict)

        self.assertIn('debug', config_data)
        self.assertFalse(config_data['debug'])

        self.assertIn('logger', config_data)
        self.assertEqual('monolog', config_data['logger'])


    def test_invalid_config(self):
        config_file = base_path + '/static/config_invalid.yml'
        specs_file = base_path + '/static/specs.yml'

        with self.assertRaisesRegex(ValueError, "'abc' is not of type 'boolean'"):
            Reader().parse(config_file, specs_file)


    def test_invalid_config_no_specs(self):
        config_file = base_path + '/static/config_invalid.yml'

        cf = Reader()
        config_data = cf.parse(config_file)
        self.assertIsInstance(config_data, dict)

        self.assertIn('debug', config_data)
        self.assertEqual('abc', config_data['debug'])


if __name__ == "__main__":
    unittest.main()
