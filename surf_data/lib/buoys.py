"""
Grab buoy data from noaa.gov.
We'll parse out the station data in this file and
return a dict of all the possible current metrics.

Station IDs for neaby Pacifica are:
{
    46237: outside Golden Gate - north of Pacifica.
           Might be the best indication of Pacifica Conditions,
    46026: east of farallones - Northwest of Pacifica,
    46012: way southwest of Pacifica
}

For a given buoy ID (station) we'll grab the raw data for
 - weather (.txt)
 - waves   (.spec)

For an explanation of wave object terms, see:
https://www.ndbc.noaa.gov/waveobs.shtml

For a general explanation of measurements and abbreviations, see:
https://www.ndbc.noaa.gov/measdes.shtml

For a guide to raw data available see:
https://www.ndbc.noaa.gov/docs/ndbc_web_data_guide.pdf
"""

from asyncio import gather
import re
from datetime import datetime
from dataclasses import dataclass
from aiohttp import ClientSession
import logging
from typing import List, Literal, Optional, Type, TypeVar, Union
from enum import Enum
from surf_data.lib.time_helpers import get_current_time, UTC_TIME_ZONE
from surf_data.lib.record_helpers import DataPoint


NDBC_BASE_URL = "https://www.ndbc.noaa.gov/data/realtime2/"
TAG_TO_ATTRIBUTE_MAP = {
    "Wind Direction (WDIR):": "wind_direction",
    "Wind Speed (WSPD):": "wind_speed",
    "Wind Gust (GST):": "wind_gust",
    "Atmospheric Pressure (PRES):": "atmospheric_pressure",
    "Air Temperature (ATMP):": "air_temperature",
    "Wind Speed at 10 meters (WSPD10M):": "wind_speed_at_10_meters",
    "Wind Speed at 20 meters (WSPD20M):": "wind_speed_at_20_meters",
    "Significant Wave Height (WVHT):": "significant_wave_height",
    "Swell Height (SwH):": "swell_height",
    "Swell Period (SwP):": "swell_period",
    "Swell Direction (SwD):": "swell_direction",
    "Wind Wave Height (WWH):": "wind_wave_height",
    "Wind Wave Period (WWP):": "wind_wave_period",
    "Wind Wave Direction (WWD):": "wind_wave_direction",
    "Wave Steepness (STEEPNESS):": "wave_steepness",
    "Average Wave Period (APD):": "average_wave_period",
}

# This is to translate the data column headers reported by NDBC
# into something more recognizable
NDBC_COL_TO_ATTRIBUTE_MAP = {
    "WDIR": "wind_direction",
    "WSPD": "wind_speed",
    "GST": "wind_gust",
    "PRES": "atmospheric_pressure",
    "ATMP": "air_temperature",
    "WTMP": "water_temperature",
    "WSPD10M": "wind_speed_at_10_meters",
    "WSPD20M": "wind_speed_at_20_meters",
    "WVHT": "significant_wave_height",
    "SwH": "swell_height",
    "SwP": "swell_period",
    "SwD": "swell_direction",
    "WWH": "wind_wave_height",
    "WWP": "wind_wave_period",
    "WWD": "wind_wave_direction",
    "STEEPNESS": "wave_steepness",
    "APD": "average_wave_period",
}


class NDBCDataTypes(Enum):
    weather = "weather"
    waves = "waves"


def parse_report_header(raw_report_header: str) -> List[str]:
    """
    Report headers always start with a '#'
    """
    processed_header_row = raw_report_header.replace("#", "").strip()
    processed_headers = re.split(r"\s+", processed_header_row)
    return [col.strip() for col in processed_headers]


def get_closest_record(
    report: "RawReport", desired_time: datetime
) -> Union["RawWeatherRecord", "RawWaveRecord"]:
    """
    Takes a datetime and returns the closest report record we can
    to that datetime.
    The dates of the report are in time order, so once we pass the minimum
    we can stop searching
    """
    min_date_diff = float("inf")
    desired_seconds = desired_time.timestamp()
    for rec in report.report_records:
        rec_date = datetime(
            int(rec.YY.measure),
            int(rec.MM.measure),
            int(rec.DD.measure),
            int(rec.hh.measure),
            int(rec.mm.measure),
            tzinfo=UTC_TIME_ZONE,  # Buoy data is in UTC
        ).timestamp()
        if abs(rec_date - desired_seconds) > min_date_diff:
            break
        current_rec = rec
        min_date_diff = abs(rec_date - desired_seconds)
    return current_rec


@dataclass
class BaseRecord:
    YY: DataPoint
    MM: DataPoint
    DD: DataPoint
    hh: DataPoint
    mm: DataPoint


@dataclass
class RawWeatherRecord(BaseRecord):
    WDIR: Optional[DataPoint] = None
    WSPD: Optional[DataPoint] = None
    GST: Optional[DataPoint] = None
    WVHT: Optional[DataPoint] = None
    DPD: Optional[DataPoint] = None
    APD: Optional[DataPoint] = None
    MWD: Optional[DataPoint] = None
    PRES: Optional[DataPoint] = None
    ATMP: Optional[DataPoint] = None
    WTMP: Optional[DataPoint] = None
    DEWP: Optional[DataPoint] = None
    VIS: Optional[DataPoint] = None
    PTDY: Optional[DataPoint] = None
    TIDE: Optional[DataPoint] = None


@dataclass
class RawWaveRecord(BaseRecord):
    WVHT: Optional[DataPoint] = None
    SwH: Optional[DataPoint] = None
    SwP: Optional[DataPoint] = None
    WWH: Optional[DataPoint] = None
    WWP: Optional[DataPoint] = None
    SwD: Optional[DataPoint] = None
    WWD: Optional[DataPoint] = None
    STEEPNESS: Optional[DataPoint] = None
    APD: Optional[DataPoint] = None
    MWD: Optional[DataPoint] = None


T = TypeVar("T", RawWaveRecord, RawWeatherRecord)


@dataclass
class RawReport:
    report_records: Union[List[RawWeatherRecord], List[RawWaveRecord]]

    @classmethod
    def from_raw_report(
        cls,
        raw_report: str,
        report_class: Type[T],
    ) -> "RawReport":
        report_lines = raw_report.splitlines()
        header = parse_report_header(report_lines[0])
        units = parse_report_header(report_lines[1])
        report_records: List[T] = []
        for record in report_lines[2:]:
            processed_record = re.split(r"\s+", record)
            report_records.append(
                report_class(
                    **{
                        header[i]: DataPoint(processed_record[i], units[i])
                        for i in range(len(processed_record))
                        if processed_record[i] != "MM"
                    }
                )
            )
        return cls(report_records=report_records)


@dataclass
class ConditionReport:
    station_id: int
    wind_direction: Optional[DataPoint] = None
    wind_speed: Optional[DataPoint] = None
    wind_gust: Optional[DataPoint] = None
    atmospheric_pressure: Optional[DataPoint] = None
    air_temperature: Optional[DataPoint] = None
    wind_speed_at_10_meters: Optional[DataPoint] = None
    wind_speed_at_20_meters: Optional[DataPoint] = None
    significant_wave_height: Optional[DataPoint] = None
    swell_height: Optional[DataPoint] = None
    swell_period: Optional[DataPoint] = None
    swell_direction: Optional[DataPoint] = None
    wind_wave_height: Optional[DataPoint] = None
    wind_wave_period: Optional[DataPoint] = None
    wind_wave_direction: Optional[DataPoint] = None
    wave_steepness: Optional[DataPoint] = None
    average_wave_period: Optional[DataPoint] = None

    def parse_raw_record_data(
        self, raw_record: Union[RawWeatherRecord, RawWaveRecord]
    ) -> None:
        """
        Looks for attributes of the report and set
        the matching ones in the ConditionReport
        """
        for raw_attr, combined_attribute in NDBC_COL_TO_ATTRIBUTE_MAP.items():
            if hasattr(raw_record, raw_attr):
                setattr(self, combined_attribute, getattr(raw_record, raw_attr))

    def serialize_for_alexa(self) -> str:
        return (
            f"The wind is coming from {self.wind_direction} with speed {self.wind_speed} and gusts up to {self.wind_gust}. "
            f'The main swell is from {self.swell_direction} and is {self.swell_height} at {self.swell_period}. <break time=".5s"/>'
            f'Secondary swell is from {self.wind_wave_direction} and is {self.wind_wave_height} at {self.wind_wave_period}. <break time=".5s"/>'
            f"Wave steepness is {self.wave_steepness or 'missing'}. "
        ).replace(" kts", " knots")


async def _get_raw_station_data(
    session: ClientSession,
    station_id: int,
    report_type: Literal[NDBCDataTypes.waves, NDBCDataTypes.weather],
) -> str:
    """
    gets the raw weather data from NDBC at a URL like this:
    https://www.ndbc.noaa.gov/data/realtime2/14040.txt
    """
    if report_type not in (NDBCDataTypes.weather, NDBCDataTypes.waves):
        raise ValueError(
            "Supplied report_type must be either "
            f"{NDBCDataTypes.weather} or {NDBCDataTypes.waves}. "
            f"Got {report_type}"
        )
    report_to_extension_map = {
        NDBCDataTypes.weather.value: "txt",
        NDBCDataTypes.waves.value: "spec",
    }
    station_url = (
        f"{NDBC_BASE_URL}{station_id}.{report_to_extension_map[report_type.value]}"
    )
    logging.info(f"Hitting: {station_url}")
    async with session.get(station_url) as resp:
        return await resp.text()


async def get_station_data(
    session: ClientSession, station_id: int, rep_time: Optional[datetime] = None
) -> ConditionReport:
    raw_weather, raw_waves = await gather(
        _get_raw_station_data(session, station_id, NDBCDataTypes.weather),
        _get_raw_station_data(session, station_id, NDBCDataTypes.waves),
    )
    if rep_time is None:
        rep_time = get_current_time()
    condition_report = ConditionReport(station_id=station_id)
    weather_report = RawReport.from_raw_report(raw_weather, RawWeatherRecord)
    wave_report = RawReport.from_raw_report(raw_waves, RawWaveRecord)
    weather_record = get_closest_record(weather_report, rep_time)
    wave_record = get_closest_record(wave_report, rep_time)
    condition_report.parse_raw_record_data(weather_record)
    condition_report.parse_raw_record_data(wave_record)
    return condition_report
