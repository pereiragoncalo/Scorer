"""Server-only Play purchase verification and short-lived signed offline licences.

Never package this module, ADC credentials or the RSA private key in the app.
A deployment still requires HTTPS, secret management, rate limiting and monitoring.
"""
import base64
import json
import os
import re
import time
import uuid
from urllib.parse import quote

PACKAGE = 'com.clemir.striker'
PRODUCT = 'scorer_world_upgrade'
TTL = 7 * 24 * 3600


class Denied(Exception):
    """Authoritative Google response: this token does not grant World."""


class Unavailable(Exception):
    """Network/configuration failure; must never grant a new licence."""


def validate_request(data):
    if not isinstance(data, dict) or set(data) != {'package', 'product', 'purchase_token', 'installation', 'nonce'}:
        raise ValueError('Invalid request schema')
    if data['package'] != PACKAGE or data['product'] != PRODUCT:
        raise ValueError('Unsupported product')
    token = data['purchase_token']
    if not isinstance(token, str) or not 20 <= len(token) <= 4096 or not re.fullmatch(r'[A-Za-z0-9._~+/=:-]+', token):
        raise ValueError('Invalid purchase token')
    for field in ('installation', 'nonce'):
        if not isinstance(data[field], str) or str(uuid.UUID(data[field])) != data[field]:
            raise ValueError('Invalid request identifier')
    return data


class GooglePlay:
    """ADC identity stays on the server; no service-account JSON is accepted by the app."""
    def __init__(self, session=None):
        if session is None:
            import google.auth
            from google.auth.transport.requests import AuthorizedSession
            credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/androidpublisher'])
            session = AuthorizedSession(credentials)
        self.session = session

    def path(self, token):
        return ('https://androidpublisher.googleapis.com/androidpublisher/v3/applications/'
                + PACKAGE + '/purchases/products/' + PRODUCT + '/tokens/' + quote(token, safe=''))

    def get(self, token):
        try:
            response = self.session.get(self.path(token), timeout=15)
            if response.status_code in (400, 404, 410):
                raise Denied()
            if response.status_code != 200:
                raise Unavailable()
            return response.json()
        except (Denied, Unavailable):
            raise
        except Exception:
            raise Unavailable() from None

    def acknowledge(self, token):
        try:
            response = self.session.post(self.path(token) + ':acknowledge', json={}, timeout=15)
            if response.status_code not in (200, 204):
                # Concurrent retry may already have acknowledged. Confirm Google state.
                if self.get(token).get('acknowledgementState') != 1:
                    raise Unavailable()
        except (Denied, Unavailable):
            raise
        except Exception:
            raise Unavailable() from None


class LicenceService:
    def __init__(self, google, private_key, *, allow_test=False, clock=time.time):
        from cryptography.hazmat.primitives.asymmetric import rsa
        if not isinstance(private_key, rsa.RSAPrivateKey) or private_key.key_size < 2048:
            raise ValueError('RSA signing key of at least 2048 bits required')
        self.google, self.private_key = google, private_key
        self.allow_test, self.clock = allow_test, clock

    def issue(self, raw):
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        request = validate_request(raw)
        token = request['purchase_token']
        result = self.google.get(token)
        # 0 PURCHASED, 1 CANCELLED, 2 PENDING. Never grant pending or consumed purchases.
        if (not isinstance(result, dict) or type(result.get('purchaseState')) is not int
                or result['purchaseState'] != 0 or type(result.get('consumptionState')) is not int
                or result.get('consumptionState') != 0
                or result.get('quantity', 1) != 1 or result.get('purchaseType') == 2
                or (result.get('purchaseType') == 0 and not self.allow_test)):
            raise Denied()
        state = result.get('acknowledgementState')
        if type(state) is not int or state not in (0, 1):
            raise Denied()
        if state == 0:
            self.google.acknowledge(token)
        now = int(self.clock())
        payload = json.dumps({'version': 1, 'package': PACKAGE, 'product': PRODUCT,
                              'installation': request['installation'], 'nonce': request['nonce'],
                              'issued_at': now, 'expires_at': now + TTL},
                             sort_keys=True, separators=(',', ':')).encode()
        signature = self.private_key.sign(payload, padding.PKCS1v15(), hashes.SHA256())
        return {'payload': base64.b64encode(payload).decode(),
                'signature': base64.b64encode(signature).decode()}


def load_service():
    from pathlib import Path
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    # Key path is supplied by deployment secret manager, never committed or printed.
    key = load_pem_private_key(Path(os.environ['SCORER_LICENSE_PRIVATE_KEY']).read_bytes(), password=None)
    return LicenceService(GooglePlay(), key, allow_test=os.environ.get('SCORER_ALLOW_TEST_PURCHASES') == '1')


_service = None


def application(environ, start_response):
    """Small WSGI endpoint. Do not use a development HTTP server in production."""
    global _service
    status = '200 OK'
    result = None
    try:
        if environ.get('REQUEST_METHOD') != 'POST' or environ.get('PATH_INFO') != '/v1/world/verify':
            status, result = '404 Not Found', {'error': 'not_found'}
        else:
            size = int(environ.get('CONTENT_LENGTH', '0'))
            if not 0 < size <= 8192 or environ.get('CONTENT_TYPE', '').split(';')[0] != 'application/json':
                raise ValueError()
            raw = environ['wsgi.input'].read(size)
            if len(raw) != size:
                raise ValueError()
            data = validate_request(json.loads(raw))
            if _service is None:
                try:
                    _service = load_service()
                except Exception:
                    raise Unavailable() from None
            result = _service.issue(data)
    except (ValueError, TypeError, UnicodeError, KeyError):
        status, result = '400 Bad Request', {'error': 'invalid_request'}
    except Denied:
        status, result = '403 Forbidden', {'error': 'not_owned'}
    except Exception:
        # Never expose token-bearing URLs, credentials or upstream responses in logs/errors.
        status, result = '503 Service Unavailable', {'error': 'verification_unavailable'}
    payload = json.dumps(result, separators=(',', ':')).encode()
    start_response(status, [('Content-Type', 'application/json'), ('Content-Length', str(len(payload))),
                            ('Cache-Control', 'no-store'), ('X-Content-Type-Options', 'nosniff')])
    return [payload]
