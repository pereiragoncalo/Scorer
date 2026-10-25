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


def configure_shared_native_distribution():
    # Buildozer normally assumes the Python distribution has the app's package
    # name. Our two APK identities share compatible compiled Python/Kivy libs.
    # Keep its path lookup in agreement with p4a's explicit --dist_name argument.
    from buildozer.targets.android import TargetAndroid
    original = TargetAndroid.get_dist_dir
    def get_dist_dir(target, dist_name):
        shared = target.buildozer.config.getdefault('app', 'scorer.shared_native_dist', '')
        if shared and shared != 'striker':
            raise ValueError('Unexpected shared native distribution')
        return original(target, shared or dist_name)
    TargetAndroid.get_dist_dir = get_dist_dir


if __name__ == '__main__':
    configure_shared_native_distribution()
    WorkspaceBuildozer().run_command(sys.argv[1:])
