"""Buildozer entry point with a writable cache, without changing HOME."""
import os
from pathlib import Path
import sys
from buildozer import Buildozer


def normalize_manifest_args(command):
    """Buildozer quotes XML for a shell, but p4a receives an argv list.

    Remove only its two known XML wrappers; never interpret shell syntax or
    unquote other arguments. Otherwise release application attributes are invalid.
    """
    if not isinstance(command, (list, tuple)):
        return command
    result = []
    for argument in command:
        for option in ('--extra-manifest-xml=', '--extra-manifest-application-arguments='):
            if isinstance(argument, str) and argument.startswith(option):
                value = argument[len(option):]
                if len(value) >= 2 and value[0] == value[-1] == '"':
                    argument = option + value[1:-1].replace('\\"', '"')
                break
        result.append(argument)
    return result


class WorkspaceBuildozer(Buildozer):
    def cmd(self, command, **kwargs):
        return super().cmd(normalize_manifest_args(command), **kwargs)

    def log_env(self, level, env):
        """Never dump process credentials when a build command fails."""
        self.error("Environment values omitted from build logs")

    @property
    def global_buildozer_dir(self):
        return str(Path(os.environ.get('STRIKER_BUILD_CACHE',
                                      '/workspace/striker-build-cache')).resolve())


if __name__ == '__main__':
    WorkspaceBuildozer().run_command(sys.argv[1:])
