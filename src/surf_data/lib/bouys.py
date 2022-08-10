"""
Grab bouy data from noaa.gov.
We'll parse out the station data in this file and
return a dict of all the possible current metrics.

Station IDs for neaby Pacifica are:
{
    46237: outside Golden Gate - north of Pacifica.
           Might be the best indication of Pacifica Conditions,
    46026: east of farallones - Northwest of Pacifica,
    46012: way southwest of Pacifica
}

For an explanation of terms, see
https://www.ndbc.noaa.gov/waveobs.shtml

"""

from bs4 import BeautifulSoup
from dataclasses import dataclass
from aiohttp import ClientSession
import logging
from typing import Optional


STATION_BASE_URL = "https://www.ndbc.noaa.gov/station_page.php?station={station_id}&tz=STN"


@dataclass
class ConditionReport:
    station_id: int
    wind_direction: Optional[str] = None
    wind_speed: Optional[str] = None
    wind_gust: Optional[str] = None
    atmospheric_pressure: Optional[str] = None
    air_temperature: Optional[str] = None
    wind_speed_at_10_meters: Optional[str] = None
    wind_speed_at_20_meters: Optional[str] = None
    significant_wave_height: Optional[str] = None
    swell_height: Optional[str] = None
    swell_period: Optional[str] = None
    swell_direction: Optional[str] = None
    wind_wave_height: Optional[str] = None
    wind_wave_period: Optional[str] = None
    wind_wave_direction: Optional[str] = None
    wave_steepness: Optional[str] = None
    average_wave_period: Optional[str] = None

    def serialize_for_alexa(self) -> str:
        return (
            f"The wind is coming from {self.wind_direction} with speed {self.wind_speed} and gusts up to {self.wind_gust}. "
            f"The main swell is from {self.swell_direction} and is {self.swell_height} at {self.swell_period}. <break time=\"1s\"/>"
            f"Secondary swell is from {self.wind_wave_direction} and is {self.wind_wave_height} at {self.wind_wave_period}. <break time=\"1s\"/>"
            f"Wave steepness is {self.wave_steepness or 'missing'}. "
        )


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


async def _scrape_station_data(session: ClientSession, station_id: int) -> str:
    station_url = STATION_BASE_URL.format(station_id=station_id)
    logging.info(f"Hitting: {station_url}...")
    async with session.get(station_url) as resp:
        return await resp.text()


async def get_station_data(session: ClientSession, station_id: int) -> ConditionReport:
    report = ConditionReport(station_id=station_id)
    station_data = await _scrape_station_data(session, station_id)
    soup = BeautifulSoup(station_data, "html.parser")
    summary_tables = soup.find_all(_find_summary_tables)
    for table in summary_tables:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            for i, cell in enumerate(cells):
                if cell.get_text() in TAG_TO_ATTRIBUTE_MAP:
                    report.__setattr__(
                        TAG_TO_ATTRIBUTE_MAP[cell.get_text()],
                        cells[i+1].get_text().strip()
                    ) 
    return report


def _find_summary_tables(tag):
    if (
        tag.name == "table"
        and tag.caption
        and (
            "Detailed Wave Summary" in tag.caption.text
            or
            "Conditions at" in tag.caption.text
        )
    ):
        return True
    return False
