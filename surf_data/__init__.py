from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class Spots(Enum):
    pacifica = "Pacifica State Beach"
    montara = "Montara State Beach"
    rockaway = "Rockaway State Beach"
    princeton_jetty = "Princeton Jetty"
    ocean_beach = "Ocean Beach"
    norcal_offshore = "Northern California Offshore Buoy"


@dataclass
class SurfSpotDetails:
    nbdc_buoy_id: int
    fallback_buoy_id: int
    noaa_tide_station_id: int
    surfline_spot_id: Optional[str]


pacifica_to_half_moon_bay = SurfSpotDetails(
    nbdc_buoy_id=46012,  # the half moon bay buoy seems to no longer work.
    fallback_buoy_id=46026,
    noaa_tide_station_id=9413450,
    surfline_spot_id="5842041f4e65fad6a7708976",
)

ocean_beach = SurfSpotDetails(
    nbdc_buoy_id=46237,
    fallback_buoy_id=46026,
    noaa_tide_station_id=9414290,
    surfline_spot_id="5842041f4e65fad6a77087f8",
)

# This buoy is 357 NM west of SF
# see https://www.ndbc.noaa.gov/station_page.php?station=46059
norcal_offshore = SurfSpotDetails(
    nbdc_buoy_id=46059,
    noaa_tide_station_id=9413450,
    surfline_spot_id=None,
    fallback_buoy_id=46214,
)


SPOT_MAPPING: Dict[str, SurfSpotDetails] = {
    Spots.pacifica.value: pacifica_to_half_moon_bay,
    Spots.montara.value: pacifica_to_half_moon_bay,
    Spots.rockaway.value: pacifica_to_half_moon_bay,
    Spots.princeton_jetty.value: pacifica_to_half_moon_bay,
    Spots.ocean_beach.value: ocean_beach,
    Spots.norcal_offshore.value: norcal_offshore,
}


class DynamoDBConfig:
    TABLE_NAME = "SurfDiary"
    REGION = "us-west-2"
    PARTITION_KEY = "spot_name"
    SORT_KEY = "entry_date"
