from surf_data.lib.ndbc import (
    PACIFICA_STATION_ID,
    parse_station_data,
    get_station_data,
    get_current_conditions,
)


def get_pacifica_data_and_parse() -> str:
    station_data = get_station_data(PACIFICA_STATION_ID)
    table = parse_station_data(station_data.text)
    print(table.text)


def get_pacifica_data() -> str:
    station_data = get_station_data(PACIFICA_STATION_ID)
    print(station_data.text)


if __name__ == "__main__":
    get_current_conditions()
