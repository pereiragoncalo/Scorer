"""Pure-Python Windows updater tests; do not require Kivy or Windows."""
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from desktop.updates import (
    GRACE_SECONDS, checked_release_url, check_update, read_cache,
    validate_manifest, version_tuple,
)

OFFICIAL = "https://github.com/pereiragoncalo/Scorer/releases"


def manifest(free="0.6.39", world="0.6.39", url=OFFICIAL):
    return json.dumps({"schema": 1, "windows": {
        "free": {"version": free, "url": url},
        "world": {"version": world, "url": url},
    }}).encode("utf-8")


class Response:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return io.BytesIO(self.body)

    def __exit__(self, *_):
        return False


def fetch(body):
    return lambda request, timeout: Response(body)


def offline(request, timeout):
    raise OSError("Connection unavailable")


class UpdatesTest(unittest.TestCase):
    def test_release_schema_and_versions(self):
        self.assertEqual(version_tuple("0.6.40"), (0, 6, 40))
        self.assertEqual(validate_manifest(manifest(), "world"), ("0.6.39", OFFICIAL))
        self.assertRaises(ValueError, version_tuple, "0.6.39.5")
        self.assertRaises(ValueError, version_tuple, "0.6.test")
        self.assertRaises(ValueError, validate_manifest, manifest(url="https://example.com/update.exe"), "free")
        self.assertRaises(ValueError, checked_release_url, "http://github.com/pereiragoncalo/Scorer/releases")
        self.assertRaises(ValueError, validate_manifest, b"x" * 8193, "world")

    def test_new_release_blocks_game(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "checks.json"
            result = check_update("free", "0.6.39", path=path, now=1000000000,
                                  open_url=fetch(manifest(free="0.6.40")))
            self.assertEqual(result.state, "required")
            self.assertEqual(result.latest, "0.6.40")
            self.assertIsNotNone(read_cache(path, "free"))

    def test_no_forced_update_when_current(self):
        with TemporaryDirectory() as tmp:
            r = check_update("world", "0.6.39", path=Path(tmp) / "checks.json",
                             now=1000000000, open_url=fetch(manifest()))
            self.assertEqual(r.state, "current")

    def test_offline_grace_and_expiry(self):
        with TemporaryDirectory() as tmp:
            p = Path(tmp) / "checks.json"
            ts = 1000000000
            check_update("free", "0.6.39", path=p, now=ts, open_url=fetch(manifest()))
            r = check_update("free", "0.6.39", path=p, now=ts+GRACE_SECONDS,
                             open_url=offline)
            self.assertEqual(r.state, "current")
            self.assertTrue(r.offline)
            self.assertEqual(check_update("free", "0.6.39", path=p,
                now=ts+GRACE_SECONDS+1, open_url=offline).state, "unavailable")

    def test_outdated_even_when_offline(self):
        with TemporaryDirectory() as tmp:
            p = Path(tmp) / "checks.json"
            ts = 1000000000
            check_update("free", "0.6.39", path=p, now=ts,
                         open_url=fetch(manifest(free="0.6.40")))
            r = check_update("free", "0.6.39", path=p, now=ts+GRACE_SECONDS+100,
                             open_url=offline)
            self.assertEqual(r.state, "required")

    def test_first_launch_without_network_is_blocked(self):
        with TemporaryDirectory() as tmp:
            r = check_update("free", "0.6.39", path=Path(tmp)/"checks.json",
                             now=1000000000, open_url=offline)
            self.assertEqual(r.state, "unavailable")

    def test_caches_are_edition_scoped(self):
        with TemporaryDirectory() as tmp:
            p = Path(tmp) / "checks.json"
            check_update("free", "0.6.39", path=p, now=1000000000, open_url=fetch(manifest()))
            r = check_update("world", "0.6.39", path=p, now=1000000010, open_url=offline)
            self.assertEqual(r.state, "unavailable")


if __name__ == "__main__":
    unittest.main()
