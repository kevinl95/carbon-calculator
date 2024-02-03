import subprocess
import json
import sqlite3
from os.path import isfile, getsize
from .exceptions import CarbonCalculatorException


class LighthouseService(object):
    """Weigh Calculator component

    It collects metrics on websites throgh the external **lighthouse**
    opensource tool

    https://github.com/GoogleChrome/lighthouse
    """

    def __init__(self, lighthouse_path: str = "") -> None:
        self._resources = {}
        self._transfered_bytes = 0
        self._resources_bytes = 0
        self._lighthouse_path = (
            lighthouse_path if lighthouse_path != "" else "lighthouse"
        )
        self._result = {}

    def analyze(self, url) -> None:
        """Collect resources data and calculates the total of transfered bytes

        Parameters
        ----------
        url : str
            The Website to analyze
        """
        try:

            cmd = f"{self._lighthouse_path} --quiet --no-update-notifier --no-enable-error-reporting --output=json --chrome-flags='--headless' {url} --only-audits='network-requests' --plugins=lighthouse-plugin-greenhouse"

            process = subprocess.Popen(
                cmd,
                shell=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            (output, error) = process.communicate()
            if not error:
                self._build_metrics(output)
            else:
                raise CarbonCalculatorException(
                    "Error in Lighthouse tool - the tool must be installed and present in the PATH or the absolute URL must be passed as argument"
                )

        except CarbonCalculatorException as e:
            raise Exception(e)

        finally:
            process.stdout.close()
            process.stderr.close()
            process.terminate()
            process.kill()

    def _build_metrics(self, output):
        mime_types = [
            "html",
            "css",
            "javascript",
            "image",
            "font",
            "audio",
            "video",
            "other",
        ]
        output = json.loads(output)
        print(output)
        items = output["audits"]["network-requests"]["details"]["items"]
        metrics = {}
        metrics["transfer_size_bytes"] = {}
        metrics["transfer_size_bytes"]["total"] = 0
        metrics["transfer_size_bytes"]["total_weighted"] = 0

        metrics["resources_size_bytes"] = {}
        metrics["resources_size_bytes"]["total"] = 0

        for mime in mime_types:
            metrics["transfer_size_bytes"][f"{mime}"] = 0
            metrics["resources_size_bytes"][f"{mime}"] = 0

        for metadata in items:
            found_mime_transfer = False
            if metadata["transferSize"] > 0:
                metrics["transfer_size_bytes"]["total"] += metadata["transferSize"]
                for mime in mime_types:
                    if mime in metadata["mimeType"]:
                        metrics["transfer_size_bytes"][f"{mime}"] += metadata[
                            "transferSize"
                        ]
                        found_mime_transfer = True
                        break
                if not found_mime_transfer:
                    metrics["transfer_size_bytes"]["other"] += metadata["transferSize"]

            found_mime_resource = False
            if metadata["resourceSize"] > 0:
                metrics["resources_size_bytes"]["total"] += metadata["resourceSize"]
                for mime in mime_types:
                    if mime in metadata["mimeType"]:
                        metrics["resources_size_bytes"][f"{mime}"] += metadata[
                            "resourceSize"
                        ]
                        found_mime_resource = True
                        break
                if not found_mime_resource:
                    metrics["resources_size_bytes"]["other"] += metadata["resourceSize"]

        self._resources = metrics

    @property
    def transfered_bytes(self) -> int:
        """The total of bytes transfered"""
        return self._transfered_bytes

    @property
    def resources_bytes(self) -> int:
        return self._resources_bytes

    @property
    def resources(self) -> dict:
        """The collection of the metrics"""
        return self._resources
