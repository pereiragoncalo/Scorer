"""Build diagnostics must not disclose credentials."""
import runpy
from pathlib import Path
import sys
import types
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


if __name__ == '__main__':
    unittest.main()
