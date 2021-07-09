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

import requests
from bs4 import BeautifulSoup, Tag
from typing import Dict, Union, Callable

PACIFICA_STATION_ID = 46012
STATION_BASE_URL = "https://www.ndbc.noaa.gov/station_page.php?station={station_id}"


def get_station_data(station_id: int) -> Dict[str, Union[str, int]]:
    station_url = STATION_BASE_URL.format(station_id=station_id)

    station_data = requests.get(station_url)
    station_data.raise_for_status()
    return station_data.text


def parse_station_data(station_data: str, parse_function: Callable[[Tag], bool]) -> Tag:
    soup = BeautifulSoup(station_data, "html.parser")
    summary_table = soup.find(parse_function)
    return summary_table


def get_current_conditions():
    station_data = get_station_data(PACIFICA_STATION_ID)
    current_conditions_tag = parse_station_data(
        station_data, find_current_conditions_table
    )
    for tx in current_conditions_tag.find_all("tr"):
        print(tx.text, "---------\n\n\n")
    # print(current_conditions_tag)
    # return current_conditions_tag


def find_wave_stats_table(tag: Tag) -> bool:
    if (
        tag.name == "table"
        and tag.caption
        and "Detailed Wave Summary" in tag.caption.text
    ):
        return True
    return False


def find_current_conditions_table(tag: Tag) -> bool:
    if (
        tag.name == "table"
        and tag.caption
        and "Detailed Wave Summary" in tag.caption.text
    ):
        return True
    return False
