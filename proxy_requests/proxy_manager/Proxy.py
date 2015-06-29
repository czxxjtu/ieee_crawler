

import urllib.request as req
import urllib.error

class Proxy:
    """
    A class of proxy
    """
    def __init__(self, ip=None, port=None, location=None, anonymous=None, protocol=None,
                 passed=0, tests=0, recent_fails=0):
        self.ip = ip
        self.port = port
        self.location = location
        self.anonymous = anonymous
        self.protocol = protocol
        self.passed = passed
        self.tests = tests
        self.recent_fails = recent_fails


    def __str__(self):
        return ''.join([self.protocol, '://', self.ip, ':', self.port])

    @property
    def empty(self):
        """
        Properties of proxy has been set or not.
        :return:
        """
        return (self.ip is None) or (self.port is None) or (self.protocol is None)


    def validate(self, url='https://twitter.com'):
        """
        Verify the proxy is working or not.
        :param url:
        :return: True or False
        """
        try:
            proxy = req.ProxyHandler({'http': str(self),
                                      'https': str(self)})
            opener = req.build_opener(proxy)
            opener.open(url)
        except urllib.error.HTTPError as e:
            return False
        except Exception as e:
            return False
        else:
            return True
