"""
Get some data from the Surfline API.
We'll see how it compares to the raw buoy and tide data.

https://services.surfline.com/kbyg/spots/forecasts/{type}?{params}

For reference, I believe kbyg stands for "Know Before You Go," which is their tagline.

Type	Data
wave	array of min/max sizes & optimal scores
wind	array of wind directions/speeds & optimal scores
tides	array of types & heights
weather	array of sunrise/set times, array of temperatures/weather conditions


days	integer	Number of forecast days to get (Max 6 w/o access token, Max 17 w/ premium token)
intervalHours	integer	Minimum of 1 (hour)
maxHeights	boolean	true seems to remove min & optimal values from the wave data output
sds	boolean	If true, use the new LOTUS forecast engine
accesstoken	string	Auth token to get premium data access (optional)

"""



# from datetime import datetime
# from aiohttp import ClientSession
# from dataclasses import dataclass
# from typing import Any, Dict, List, Literal, Union
# import asyncio


# SURFLINE_URL = "https://services.surfline.com/kbyg/spots/forecasts/"
# SURFLINE_API_DEFAULT_PARAMS = dict(
#     days=1,
#     intervalHours=1,
#     maxHeights="False",
#     sds="False",
# )

# @dataclass
# class SurflineTide:
#     timestamp: datetime
#     tide_type: Literal["NORMAL", "LOW", "HIGH"]
#     height: float

#     @classmethod
#     def from_tide_dict(cls, tide_dict: Dict[str, Any]) -> "SurflineTide":
#         return cls(
#             timestamp=datetime.fromtimestamp(tide_dict["timestamp"]),
#             tide_type=tide_dict["type"],
#             height=tide_dict["height"]
#         )

# @dataclass
# class SurflineTides:
#     units: Dict[str, str]
#     tide_location: Dict[str, Union[str, float]]
#     tides: List[SurflineTide]

#     @classmethod
#     def from_tide_report(cls: "SurflineTides", tide: Dict[str, Any]) -> "SurflineTides":
#         """
#         Parses the results from the Surfline tide API to return a
#         SurflineTide object
#         """
#         return cls(
#             units=tide["units"],
#             tide_location=tide["data"]["tideLocation"],
#             tides=[SurflineTide.from_tide_dict(tide) for tide in tide["data"]["tides"]]
#         )


# @dataclass
# class SurflineWaves:
#     wave: Any

# @dataclass
# class SurflineWeather:
#     weather: Any

# @dataclass
# class SurflineWind:
#     wind: Any




# class SurflineSpots:
#     linda_mar = "5842041f4e65fad6a7708976"


# async def get_tide_data(session: ClientSession, spot_id: str) -> SurflineTides:
#     params = dict(
#         spotId=spot_id,
#         **SURFLINE_API_DEFAULT_PARAMS
#     )
#     async with session.get(SURFLINE_URL, params=params) as resp:
#         tide_data = await resp.json()
#     return SurflineTides.from_tide_report(tide_data)

# async def get_wave_data() -> SurflineWaves:
#     ...

# async def get_wind_data() -> SurflineWind:
#     ...

# async def get_weather_data() -> SurflineWeather:
#     ...

# async def get_data() -> SurflineTides:
#     async with ClientSession() as session:
#         results = await asyncio.gather(
#             get_tide_data(session, SurflineSpots.linda_mar)
#         )
#     return results[0]

# if __name__ == "__main__":
#     tides = asyncio.run(get_data())
#     print(tides.tides.json())
