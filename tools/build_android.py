"""Buildozer entry point with a writable cache, without changing HOME."""
import os
from pathlib import Path
import sys
from buildozer import Buildozer


class WorkspaceBuildozer(Buildozer):
    @property
    def global_buildozer_dir(self):
        return str(Path(os.environ.get('STRIKER_BUILD_CACHE',
                                      '/workspace/striker-build-cache')).resolve())


if __name__ == '__main__':
    WorkspaceBuildozer().run_command(sys.argv[1:])
