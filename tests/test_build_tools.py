"""Build diagnostics must not disclose credentials."""
import runpy
from pathlib import Path
import sys
import types
import tempfile
import configparser
import unittest
from unittest.mock import patch


class BuildLogTests(unittest.TestCase):
    def test_failure_logging_omits_environment_values(self):
        fake = types.ModuleType('buildozer')
        fake.Buildozer = object
        path = Path(__file__).resolve().parents[1] / 'tools/build_android.py'
        with patch.dict(sys.modules, {'buildozer': fake}):
            cls = runpy.run_path(str(path))['WorkspaceBuildozer']
        runner = cls()
        messages = []
        runner.error = messages.append
        runner.log_env(0, {'EXAMPLE_API_KEY': 'must-never-appear'})
        self.assertTrue(messages)
        self.assertNotIn('must-never-appear', '\n'.join(messages))
        self.assertNotIn('EXAMPLE_API_KEY', '\n'.join(messages))

    def test_manifest_arguments_are_xml_not_literal_shell_quotes(self):
        fake = types.ModuleType('buildozer'); fake.Buildozer = object
        path = Path(__file__).resolve().parents[1] / 'tools/build_android.py'
        with patch.dict(sys.modules, {'buildozer': fake}):
            normalize = runpy.run_path(str(path))['normalize_manifest_args']
        xml = '<uses-permission android:name="example" />'
        app = 'android:usesCleartextTraffic="false"'
        result = normalize(['python', '--extra-manifest-xml="'+xml+'"',
                            '--extra-manifest-application-arguments="'+app.replace('"', '\\"')+'"',
                            '--name', 'SCORER Play QA', '$(must-not-execute)'])
        self.assertEqual(result[1], '--extra-manifest-xml='+xml)
        self.assertEqual(result[2], '--extra-manifest-application-arguments='+app)
        self.assertEqual(result[-1], '$(must-not-execute)')
        self.assertEqual(result[-2], 'SCORER Play QA')

    def test_pip_trust_preserves_existing_settings_and_repeats(self):
        path = Path(__file__).resolve().parents[1] / 'tools/android/configure_pip_trust.py'
        configure = runpy.run_path(str(path))['configure']
        with tempfile.TemporaryDirectory() as temp:
            config_path = Path(temp) / 'pip.conf'
            config_path.write_text('[global]\ntimeout = 45\n[index]\ncustom = keep\n')
            configure(config_path)
            first = config_path.read_text()
            configure(config_path)
            self.assertEqual(config_path.read_text(), first)
            config = configparser.ConfigParser()
            config.read(config_path)
            self.assertEqual(config['global']['cert'], '/run/ca-bundle.crt')
            self.assertEqual(config['global']['timeout'], '45')
            self.assertEqual(config['index']['custom'], 'keep')
            self.assertFalse(config.has_option('global', 'trusted-host'))

    def test_invalid_pip_config_is_not_overwritten(self):
        path = Path(__file__).resolve().parents[1] / 'tools/android/configure_pip_trust.py'
        configure = runpy.run_path(str(path))['configure']
        with tempfile.TemporaryDirectory() as temp:
            config_path = Path(temp) / 'pip.conf'
            config_path.write_text('not a valid configuration')
            with self.assertRaises(configparser.Error):
                configure(config_path)
            self.assertEqual(config_path.read_text(), 'not a valid configuration')

    def test_java_uses_managed_proxy_and_keeps_tls_trust(self):
        path = Path(__file__).resolve().parents[1] / 'tools/android/java_proxy_options.py'
        options = runpy.run_path(str(path))['options']
        result = options({'HTTPS_PROXY': 'http://proxy.example:8080'})
        self.assertIn('-Dhttps.proxyHost=proxy.example', result)
        self.assertIn('-Dhttps.proxyPort=8080', result)
        self.assertIn('-Djavax.net.ssl.trustStore=', result)

    def test_java_does_not_expose_proxy_credentials(self):
        path = Path(__file__).resolve().parents[1] / 'tools/android/java_proxy_options.py'
        options = runpy.run_path(str(path))['options']
        with self.assertRaisesRegex(ValueError, 'managed unauthenticated') as caught:
            options({'HTTPS_PROXY': 'http://username:private-value@proxy.example:8080'})
        self.assertNotIn('private-value', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
