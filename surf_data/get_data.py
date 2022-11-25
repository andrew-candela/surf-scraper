from surf_data.lib.buoys import get_station_data, ConditionReport
from surf_data.lib.tides import TideData, get_tide_data
from surf_data.lib.time_helpers import get_current_time
from surf_data import SPOT_MAPPING, Spots
import asyncio
from aiohttp import ClientSession
from datetime import datetime
from typing import Optional


async def get_spot_data(
    spot_name: str, start_time: Optional[datetime] = None
) -> tuple[ConditionReport, TideData]:
    surf_spot = SPOT_MAPPING[spot_name]
    if start_time is None:
        start_time = get_current_time()
    async with ClientSession(raise_for_status=True) as session:
        results = await asyncio.gather(
            get_station_data(session, surf_spot.nbdc_buoy_id, start_time),
            get_tide_data(session, surf_spot.noaa_tide_station_id, start_time),
        )
    return results


if __name__ == "__main__":
    # from surf_data.lib.time_helpers import PST_TIME_ZONE

    conditions, tide = asyncio.run(
        # get_spot_data(
        #     Spots.pacifica.value, datetime(2022, 9, 10, 17, tzinfo=PST_TIME_ZONE)
        # )
        get_spot_data(Spots.pacifica.value)
    )
    print(conditions.serialize_for_alexa())
