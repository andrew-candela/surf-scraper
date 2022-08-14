from surf_data.lib.bouys import get_station_data, ConditionReport
from surf_data.lib.tides import TideData, get_tide_data
from surf_data.lib.time_helpers import get_current_time
from surf_data import SPOT_MAPPING, Spots
import asyncio
from aiohttp import ClientSession
from datetime import datetime


async def get_spot_data(spot_name: str) -> tuple[ConditionReport, TideData]:
    surf_spot = SPOT_MAPPING[spot_name]
    start_time = get_current_time()
    async with ClientSession(raise_for_status=True) as session:
        results = await asyncio.gather(
            get_station_data(session, surf_spot.nbdc_bouy_id),
            get_tide_data(session, surf_spot.noaa_tide_station_id, start_time),
        )
    return results


if __name__ == "__main__":
    conditions, tide = asyncio.run(get_spot_data(Spots.pacifica.value))
    print(tide.serialize_for_alexa())
