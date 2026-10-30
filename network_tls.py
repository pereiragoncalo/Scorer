"""Verified TLS roots: certifi where installed, bundled Mozilla CAs on Android."""
from pathlib import Path
import ssl

def verified_context():
    try:
        import certifi
        path=certifi.where()
    except ImportError:
        path=str(Path(__file__).resolve().parent/'assets/network/mozilla-ca.crt')
    return ssl.create_default_context(cafile=path)
