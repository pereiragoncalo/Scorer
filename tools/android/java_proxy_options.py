"""Map the managed proxy to Java's supported proxy properties, keeping TLS on."""
import os
from urllib.parse import urlparse


def options(environ):
    result = ['-Djavax.net.ssl.trustStore=/work/cache/java-cacerts']
    for protocol in ('http', 'https'):
        value = environ.get(protocol.upper() + '_PROXY') or environ.get(protocol + '_proxy')
        if not value:
            continue
        proxy = urlparse(value)
        if proxy.scheme != 'http' or not proxy.hostname or proxy.username or proxy.password:
            raise ValueError('Java proxy requires the managed unauthenticated HTTP endpoint')
        result += [f'-D{protocol}.proxyHost={proxy.hostname}',
                   f'-D{protocol}.proxyPort={proxy.port or 80}']
    return ' '.join(result)


if __name__ == '__main__':
    print(options(os.environ))
