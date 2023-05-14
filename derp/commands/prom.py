import requests
import os
import time

from prometheus_pandas.query import Prometheus as PrometheusPandas


def prometheus_pandas(access_token, url):
    if not url.endswith('/'):
        url += '/'

    http = requests.Session()
    http.headers['Authorization'] = f'Bearer {access_token}'

    return PrometheusPandas(url, http)


def prometheus_pandas_from_env():
    return prometheus_pandas(os.getenv('PROMETHEUS_ACCESS_TOKEN'), os.getenv('PROMETHEUS_URL'))



class PromCommand:
    command = 'prom'

    def __init__(self):
        self._access_token = None
        self._access_token_expires_at = 0

    def access_token(self):
        # Should do this via dependency injection...

        if self._access_token and time.time() < self._access_token_expires_at:
            return self._access_token

        response = requests.post(
            f'https://login.microsoftonline.com/{os.getenv("TENANT_ID")}/oauth2/token',
            data={
                'grant_type': 'client_credentials',
                'client_id': os.getenv('CLIENT_ID'),
                'client_secret': os.getenv('CLIENT_SECRET'),
                'resource': 'https://prometheus.monitor.azure.com'
            })
        response.raise_for_status()

        result = response.json()
        self._access_token = result['access_token']
        self._access_token_expires_on = float(result['expires_on'])

        return response.json()['access_token']

    def url(self):
        return os.getenv('PROMETHEUS_URL')

    def client(self):
        access_token = self.access_token()
        url = os.getenv('PROMETHEUS_URL')
        return prometheus_pandas(access_token, url)

    def __call__(self, msg):
        parts = msg.split(' ')[1:]
        cmd = parts[0]

        if cmd == 'query':
            return self.query(parts)

        if cmd == 'query_range':
            return self.query_range(parts)

        if cmd == 'series':
            return self.series(parts)

    def query(self, parts):
        client = self.client()
        client.query()

    def query_range(self, parts):
        pass

    def series(self, parts):
        pass


