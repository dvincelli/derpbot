import arrow
from dateutil.tz import tzlocal
import io
import requests
import os
import time
from typing import Optional, Union
import matplotlib.pyplot as plt
import matplotlib.dates
from prometheus_pandas.query import Prometheus as PrometheusPandas
from datetime import datetime, timedelta
import logging
import pytz
from derp.command.response import SayArgs, SayResponse, ShareFileResponse, ShareFileArgs
import threading
import pandas as pd


logger = logging.getLogger(__name__)


plt_lock = threading.Lock()


def prometheus_pandas(access_token, url):
    if not url.endswith("/"):
        url += "/"

    http = requests.Session()
    http.headers["Authorization"] = f"Bearer {access_token}"

    return PrometheusPandas(url, http)


class PromCommand:
    command = "prom"
    wants_parse = True

    def __init__(self):
        self._access_token = None
        self._access_token_expires_at = 0

    def access_token(self):
        # Should do this via dependency injection / provider. At the very least,
        # the oauth end-point and payload needs to be configurable.

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
        df = df.tz_localize(tz=pytz.UTC)
        df = df.tz_convert(tz=tzlocal())
        logger.debug("Got df %r", df)
        return df


def save_plot(df: pd.DataFrame, kind: str = 'line'):
    with plt_lock:
        ax = plt.subplot()
        ax.xaxis.set_major_formatter(
            matplotlib.dates.DateFormatter("%m-%d %H:%M", tz=tzlocal())
        )
        ax = df.plot(kind=kind, ax=ax)

        buf = io.BytesIO()

        plt.savefig(buf, format="png")
        plt.close()

        buf.seek(0)
        return buf


class VizCommand(PromCommand):
    command = "viz"

    def query(self, *args, **kwargs):
        return super().query(*args, **kwargs)

    def query_range(self, *args, **kwargs):
        kind = kwargs.pop("kind", "line")
        df = super().query_range(*args, **kwargs)
        return save_plot(df, kind=kind)


    def __call__(self, command):
        args = command[2]

        if "query" in args:
            logger.debug("query with %r", args)
            return self.query(**args)

        if "query_range" in args:
            logger.debug("query_range with %r", args)
            title = "{query_range} from {start} to {end} in {step} steps".format(**args)
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
        response = super().__call__(
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
        now = end.format("YYYY-MM-DD HH:mm")
        response.args["title"] = f"Queue Lengths as of {now}"
        return response


class TasksCommand(PromCommand):
    command = "tasks"

    def __call__(self, command):
        end = arrow.now()
        start = end.shift(hours=-1)

        args = command[2]

        status = args.get("status", "succeeded")  # succeeded, failed, received
        tasks = args.get("tasks", ".+")  # all tasks, otherwise pipe-seperated
        step = args.get("step", "10m")

        # succeeded, failed, received
        metric = f"celery_task_{status}_total"

        response = super().__call__(
            [
                command[0],
                "tasks",
                dict(
                    query_range=f'sum by (name) (round(increase({metric}{{kubernetes_service_name=~"celery-exporter",kubernetes_namespace="default",name=~"{tasks}"}}[{step}])))',
                    start=start.isoformat(),
                    end=end.isoformat(),
                    step=step,
                ),
            ]
        )
        return response


class TaskCommand(PromCommand):
    command = "task"

    def __call__(self, command):
        end = arrow.now()
        start = end.shift(hours=-1)

        args = command[2]

        task = args.get("task", None)
        if not task:
            return SayResponse(
                SayArgs(text='Error: "task" argument missing')
            )

        step = args.get("step", "10m")

        # TODO: allow user to override the date
        # start = args.get("start", start)
        # end = args.get("end", end)

        # succeeded, failed, received

        dfs = []
        for status in ["received", "succeeded", "failed"]:
            metric = f"celery_task_{status}_total"
            query = f'sum by (name) (round(increase({metric}{{kubernetes_service_name=~"celery-exporter",kubernetes_namespace="default",name="{task}"}}[{step}])))'
            logger.debug("PromQL Query is %r", query)
            df = self.query_range(query_range=query, start=start.isoformat(), end=end.isoformat(), step=step)
            df.columns = [f'{status}']
            dfs.append(df)

        merged_df = dfs[0].join(dfs[1]).join(dfs[2])

        content = save_plot(merged_df)

        now = end.format("YYYY-MM-DD HH:mm")
        title = "{task} from {start} to {end} in {step} steps".format(task=task, start=start, end=end, step=step)
        filename = "plot.png"
        response = ShareFileResponse(
                args=ShareFileArgs(
                    title=title,
                    filename=filename,
                    content=content,
                    text="{file_url}",
                    channel=None,
                    thread_ts=None,
                )
            )
        response.args["title"] = f"{task} status as of {now}"
        return response


class K8sCommand(PromCommand):
    command = "k8s"
    wants_parse = True

    queries = {
        "cpu-idle": 'sum((rate(container_cpu_usage_seconds_total{container!="POD",container!=""}[30m]) - on (namespace,pod,container) group_left avg by (namespace,pod,container)(kube_pod_container_resource_requests{resource="cpu"})) * -1 >0)',
        "cpu-no-limit": 'count by (namespace)(sum by (namespace,pod,container)(kube_pod_container_info{container!=""}) unless sum by (namespace,pod,container)(kube_pod_container_resource_limits{resource="cpu"}))',
        "cpu-overcommit": 'sum(kube_pod_container_resource_limits{resource="cpu"}) - sum(kube_node_status_capacity{resource="cpu"})',
        "mem-idle": 'sum((container_memory_usage_bytes{container!="POD",container!=""} - on (namespace,pod,container) avg by (namespace,pod,container)(kube_pod_container_resource_requests{resource="memory"})) * -1 >0 ) / (1024*1024*1024)',
        "mem-overcommit": 'sum(kube_pod_container_resource_limits{resource="memory"}) - sum(kube_node_status_capacity{resource="memory"})',
        "node-not-ready": 'sum(kube_node_status_condition{condition="NotReady",status="true"})',
        "node-ready": 'sum(kube_node_status_condition{condition="Ready",status="true"})',
        "node-unstable": 'sum(changes(kube_node_status_condition{status="true",condition="Ready"}[15m])) by (node) > 2',
        "node-unschedulable": "sum(kube_node_spec_unschedulable) by (node)",
        "pod-count": "sum by (namespace) (kube_pod_info)",
        "pod-pending": 'kube_pod_status_phase {exported_namespace="mynamespace", phase="Pending"} > 0.',
        "pod-restarts": "increase(kube_pod_container_status_restarts_total[15m]) > 3",
        "pod-unhealthy": 'min_over_time(sum by (namespace, pod) (kube_pod_status_phase{phase=~"Pending|Unknown|Failed"})[15m:1m]) > 0',
        "pvc-pending": 'kube_persistentvolumeclaim_status_phase{phase="Pending"} > 0',
    }

    def __call__(self, cmd):
        (mention, _, args) = cmd

        if args.get("query") in self.queries:
            argz = args.copy()
            argz["query"] = self.queries.get(args["query"])
            return super().__call__([mention, "query", argz])
        else:
            return "Invalid args: %r" % args
