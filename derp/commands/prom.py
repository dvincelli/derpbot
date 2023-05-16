import arrow
import io
from numpy._typing import _256Bit
import requests
import os
import time
from typing import Optional, Union
import matplotlib.pyplot as plt
from prometheus_pandas.query import Prometheus as PrometheusPandas
from datetime import datetime, timedelta
import logging
from derp.command.response import SayResponse, ShareFileResponse, ShareFileArgs


logger = logging.getLogger(__name__)


def prometheus_pandas(access_token, url):
    if not url.endswith("/"):
        url += "/"

    http = requests.Session()
    http.headers["Authorization"] = f"Bearer {access_token}"

    return PrometheusPandas(url, http)


def prometheus_pandas_from_env():
    return prometheus_pandas(
        os.getenv("PROMETHEUS_ACCESS_TOKEN"), os.getenv("PROMETHEUS_URL")
    )


class PromCommand:
    command = "prom"
    wants_parse = True

    def __init__(self):
        self._access_token = None
        self._access_token_expires_at = 0

    def access_token(self):
        # Should do this via dependency injection / provider...

        if self._access_token and time.time() < self._access_token_expires_at:
            return self._access_token

        response = requests.post(
            f'https://login.microsoftonline.com/{os.getenv("TENANT_ID")}/oauth2/token',
            data={
                "grant_type": "client_credentials",
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
                "resource": "https://prometheus.monitor.azure.com",
            },
        )
        response.raise_for_status()

        result = response.json()
        self._access_token = result["access_token"]
        self._access_token_expires_on = float(result["expires_on"])

        return response.json()["access_token"]

    def url(self):
        return os.getenv("PROMETHEUS_URL")

    def client(self):
        access_token = self.access_token()
        url = os.getenv("PROMETHEUS_URL")
        return prometheus_pandas(access_token, url)

    def __call__(self, command):
        df = self._request(command)
        logger.debug("Returning df %s", df)
        return f"```\n{df}\n```"

    def _request(self, command):
        cmd = command[1]
        args = command[2]
        logger.debug("running %r with %r", cmd, args)

        if "query" in args:
            logger.debug("query with %r", args)
            return self.query(**args)

        if "query_range" in args:
            logger.debug("query_range with %r", args)
            return self.query_range(**args)

    def query(
        self,
        query: str,
        time: Optional[Union[int, str]] = None,
        timeout: Optional[int] = None,
    ):
        client = self.client()
        logger.debug("Got client %r", client)
        df = client.query(
            query=query,
            time=time,
            timeout=timedelta(seconds=timeout) if timeout is not None else None,
        )
        logger.debug("Got df %r", df)
        return df

    def query_range(
        self,
        query_range: str,
        start: Union[str, datetime, float],
        end: Union[str, datetime, float],
        step: str,
        timeout: Optional[int] = None,
    ):
        client = self.client()
        logger.debug("Got client %r", client)
        df = client.query_range(
            query=query_range,
            start=start,
            end=end,
            step=step,
            timeout=timedelta(seconds=timeout) if timeout is not None else None,
        )
        logger.debug("Got df %r", df)
        return df


class VizCommand(PromCommand):
    command = "viz"

    def query(self, *args, **kwargs):
        return super().query(*args, **kwargs)

    def query_range(self, *args, **kwargs):
        kind = kwargs.pop("kind", "line")
        df = super().query_range(*args, **kwargs)
        df.plot(kind=kind)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        return buf

    def __call__(self, command):
        cmd = command[1]
        args = command[2]

        if "query" in args:
            logger.debug("query with %r", args)
            return self.query(**args)

        if "query_range" in args:
            logger.debug("query_range with %r", args)
            title = "{query_range} from {start} to {end} in {step} steps".format(args)
            filename = "plot.png"
            content = self.query_range(**args)
            return ShareFileResponse(
                args=ShareFileArgs(
                    title=title,
                    filename=filename,
                    content=content,
                    text="{file_url}",
                    channel=None,
                    thread_ts=None,
                )
            )


class QueueLengths(VizCommand):
    command = "queues"

    def __call__(self, command):
        end = arrow.now()
        start = end.shift(hours=-1)
        return super().__call__(
            [
                command[0],
                "queues",
                dict(
                    query_range="sum(celery_queue_length{kubernetes_namespace='default'}) by (queue_name)",
                    start=start.isoformat(),
                    end=end.isoformat(),
                    step="1m",
                ),
            ]
        )
