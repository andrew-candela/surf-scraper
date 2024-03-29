"""
Tools for grabbing the tide data from
https://api.tidesandcurrents.noaa.gov

Base URL: https://api.tidesandcurrents.noaa.gov/api/prod/datagetter
example args: 
    product=predictions
    application=NOS.COOPS.TAC.WL
    begin_date=YYYYMMDD
    end_date=YYYYMMDD
    datum=MLLW
    station=9414131
    time_zone=lst_ldt
    units=english
    interval=hilo
    format=json

The API returns a json blob like this:
{ "predictions" : [
    {"t":"2022-08-06 00:21", "v":"0.804", "type":"L"},
    {"t":"2022-08-06 06:40", "v":"3.476", "type":"H"},
    {"t":"2022-08-06 11:04", "v":"2.591", "type":"L"},
    {"t":"2022-08-06 17:48", "v":"5.902", "type":"H"}
]}
"""

from typing import Any, Dict, List
from decimal import Decimal
from aiohttp import ClientSession
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from surf_data import SurfSpotDetails


DT_FORMAT = "%Y-%m-%d %H:%M"
DT_SHORT_FORMAT = "%Y%m%d"
NOAA_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"

STATIC_NOAA_PARAMS = {
    "product": "predictions",
    "application": "NOS.COOPS.TAC.WL",
    "datum": "MLLW",
    "time_zone": "lst_ldt",
    "units": "english",
    "interval": "h",
    "format": "json",
}


@dataclass
class TidePrediction:
    time: datetime
    level: Decimal


@dataclass
class TideData:
    tide_height: str
    tide_rate_of_change: str

    def serialize_for_alexa(self) -> str:
        tide_change = float(self.tide_rate_of_change)
        if tide_change <= 0:
            tide_diff_expression = "going out"
        else:
            tide_diff_expression = "coming in"
        return (
            f"The tide is currently {self.tide_height} feet and is {tide_diff_expression} at "
            f"{abs(tide_change)} feet per hour. "
        )


def parse_tide_prediction(prediction: Dict[str, str]) -> "TidePrediction":
    dt = datetime.strptime(prediction["t"], DT_FORMAT)
    level = Decimal(prediction["v"])
    return TidePrediction(dt, level)


def find_tide_change(
    current_minute: int, start: TidePrediction, end: TidePrediction
) -> TideData:
    tide_interval = end.level - start.level
    level = float(start.level) + (float(tide_interval) * (current_minute / 60))
    return TideData(str(round(level, 1)), str(round(tide_interval, 1)))


@dataclass
class TidePredictions:
    predictions: List[TidePrediction]

    @classmethod
    def parse_noaa_data(cls, noaa_resp: Dict[str, Any]) -> "TidePredictions":
        return TidePredictions(
            predictions=[parse_tide_prediction(p) for p in noaa_resp["predictions"]]
        )

    def compute_tide_data(self, compute_time: datetime) -> TideData:
        """
        Find the hour before and after and then compute the "slope", as well as interpolate
        current level.
        """
        rounded_time = compute_time.replace(
            minute=0, second=0, microsecond=0, tzinfo=None
        )
        for i, prediction in enumerate(self.predictions):
            if prediction.time == rounded_time:
                return find_tide_change(
                    compute_time.minute, prediction, self.predictions[i + 1]
                )
        raise ValueError(
            f"There was no hourly interval containing your time of: {compute_time}"
        )


async def get_tide_data(
    session: ClientSession, spot: SurfSpotDetails, start_date: datetime
) -> TideData:
    begin_date = start_date - timedelta(days=1)
    end_date = start_date + timedelta(days=1)
    params = dict(
        **STATIC_NOAA_PARAMS,
        station=spot.noaa_tide_station_id,
        begin_date=begin_date.strftime(DT_SHORT_FORMAT),
        end_date=end_date.strftime(DT_SHORT_FORMAT),
    )
    logging.info("Sending request to NOAA for tide data")
    async with session.get(NOAA_URL, params=params) as resp:
        tide_data = await resp.json()
    return TidePredictions.parse_noaa_data(tide_data).compute_tide_data(start_date)
