from configparser import ConfigParser
import os
from .services import LighthouseService
from .statistics import PageStatistics, StatisticsBuilder
from .exceptions import CarbonCalculatorException
import validators
from datetime import date, datetime, timezone
import json


class CarbonCalculator(object):
    """Carbon Calculator - The main module:"""

    def __init__(
        self, lighthouse: LighthouseService, reqs: int
    ) -> None:
        self._builder = StatisticsBuilder(lighthouse)
        self._statistics = None
        self._estimated_requests = reqs

    def footprint(self, url: str) -> dict:
        if not validators.url(url):
            raise CarbonCalculatorException("The URL is not valid")
        try:
            self._statistics = None
            self._statistics = self._builder.build(url)
            self._co2 = self._statistics
        except Exception as e:
            raise CarbonCalculatorException(e)

    @property
    def date(self):
        return self._statistics.created_at

    @property
    def url(self) -> str:
        return self._statistics.url

    @property
    def hosting_green(self) -> bool:
        return self._statistics.hosting_green

    @property
    def co2_grams(self) -> float:
        return self._statistics.co2_grams

    @property
    def energy_kWh(self) -> float:
        return self._statistics.energy_kWh

    @property
    def water_litres(self) -> float:
        return self._statistics.water_litres

    @property
    def transfer_size_bytes(self) -> float:
        return self._statistics.transfer_size_bytes

    @property
    def resources_size_bytes(self) -> float:
        return self._statistics.resources_size_bytes

    @property
    def resources(self) -> dict:
        return self._statistics.resources

    def to_string(self) -> str:
        output = ""
        output += "date " + str(self._statistics.created_at) + "\n"
        output += "url " + self._statistics.url + "\n"
        output += "hosting_green " + str(self._statistics.hosting_green) + "\n"
        output += "co2_grams " + str(self._statistics.co2_grams) + "\n"
        # Estimate the offset
        tons = self._statistics.co2_grams * 0.000001 * self._estimated_requests
        output += "offset_link " + "https://www.wren.co/offset-anything?amount=" + str(tons) + "&unit=ton" + "\n"
        output += "energy_kWh " + str(self._statistics.energy_kWh) + "\n"
        output += "water_litres " + str(self._statistics.water_litres) + "\n"
        output += "resources " + str(self._statistics.resources)

        return output

    def to_dict(self) -> dict:
        output = {}
        output["date"] = self._statistics.created_at
        output["url"] = self._statistics.url
        output["hosting_green"] = self._statistics.hosting_green
        output["co2_grams"] = self._statistics.co2_grams
        # Estimate the offset
        tons = self._statistics.co2_grams * 0.000001 * self._estimated_requests
        output["offset_link"] = "https://www.wren.co/offset-anything?amount=" + str(tons) + "&unit=ton"
        output["energy_kWh"] = self._statistics.energy_kWh
        output["water_litres"] = self._statistics.water_litres
        output["resources"] = self._statistics.resources

        return output

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4, default=json_serial)

    @classmethod
    def from_ini_file(cls, config_file: str) -> None:
        config = ConfigParser()
        config.read(config_file)

        lighthouse_filename = ""
        if config["LIGHTHOUSE"]["LIGHTHOUSE_PATH"] != "":
            lighthouse_filename = os.path.join(
                os.path.dirname(__file__),
                "../../",
                config["LIGHTHOUSE"]["LIGHTHOUSE_PATH"],
            )

        lighthouse = LighthouseService(lighthouse_filename)

        return cls(lighthouse=lighthouse)


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
