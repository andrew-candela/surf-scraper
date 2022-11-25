from surf_data.lib import buoys


mock_ndbc_weather_report = (
    "#YY  MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS PTDY  TIDE\n"
    "#yr  mo dy hr mn degT m/s  m/s     m   sec   sec degT   hPa  degC  degC  degC  nmi  hPa    ft\n"
    "2022 09 04 19 00 175  3.5  4.5    MM    MM    MM  MM 1013.5  24.9  26.5    MM   MM   MM    MM\n"
    "2022 09 04 18 00 183  3.6  4.9    MM    MM    MM  MM 1013.6  25.3  26.5    MM   MM   MM    MM\n"
    "2022 09 04 17 00 186  4.0  4.9    MM    MM    MM  MM 1013.7  25.4  26.5    MM   MM   MM    MM\n"
    "2022 09 04 16 00 196  4.4  5.5    MM    MM    MM  MM 1013.2  25.3  26.6    MM   MM   MM    MM\n"
    "2022 09 04 15 00 184  4.4  5.5    MM    MM    MM  MM 1012.6  24.9  26.6    MM   MM   MM    MM\n"
    "2022 09 04 14 00 254  2.3  3.4    MM    MM    MM  MM 1011.8  24.0  26.6    MM   MM   MM    MM\n"
)

mock_ndbc_wave_report = (
    "#YY  MM DD hh mm WVHT  SwH  SwP  WWH  WWP SwD WWD  STEEPNESS  APD MWD\n"
    "#yr  mo dy hr mn    m    m  sec    m  sec  -  degT     -      sec degT\n"
    "2022 09 04 22 40  2.1  1.5  9.1  1.4  7.1 WNW  NW    AVERAGE  6.1 292\n"
    "2022 09 04 21 40  2.0  1.6  8.3  1.2  6.2  NW  NW    AVERAGE  6.2 305\n"
    "2022 09 04 20 40  2.0  1.6  7.7  1.1  6.2  NW  NW      STEEP  6.1 305\n"
    "2022 09 04 16 40  1.9  1.5  9.1  1.2  5.9 WNW WNW    AVERAGE  5.7 301\n"
    "2022 09 04 14 40  1.8  1.5  7.7  1.0  5.0 WNW WNW      STEEP  5.9 298\n"
    "2022 09 04 13 40  1.9  1.5  7.1  1.1  5.9 WNW WNW      STEEP  5.9 296\n"
    "2022 09 04 12 40  1.7  1.5  7.1  0.8  4.8 WNW  NW      STEEP  6.1 302\n"
    "2022 09 04 11 40  1.7  1.6  7.7  0.6  4.3 WNW WNW      STEEP  6.3 297\n"
    "2022 09 04 09 40  1.8  1.7  6.7  0.6  4.0  NW  NW      STEEP  6.1 308\n"
    "2022 09 04 08 40  1.9  1.8  7.1  0.7  4.5  NW  NW      STEEP  6.1 305\n"
)


def test_parse_report_header():
    expected_weather_header = [
        "YY",
        "MM",
        "DD",
        "hh",
        "mm",
        "WDIR",
        "WSPD",
        "GST",
        "WVHT",
        "DPD",
        "APD",
        "MWD",
        "PRES",
        "ATMP",
        "WTMP",
        "DEWP",
        "VIS",
        "PTDY",
        "TIDE",
    ]
    expected_wave_header = [
        "YY",
        "MM",
        "DD",
        "hh",
        "mm",
        "WVHT",
        "SwH",
        "SwP",
        "WWH",
        "WWP",
        "SwD",
        "WWD",
        "STEEPNESS",
        "APD",
        "MWD",
    ]
    assert (
        buoys.parse_report_header(mock_ndbc_weather_report.splitlines()[0])
        == expected_weather_header
    )
    assert (
        buoys.parse_report_header(mock_ndbc_wave_report.splitlines()[0])
        == expected_wave_header
    )


def test_parse_raw_weather_report():
    expected_report = buoys.RawWeatherReport(
        report_records=[
            buoys.RawWeatherRecord(
                YY="2022",
                MM="09",
                DD="04",
                hh="19",
                mm="00",
                WDIR="175",
                WSPD="3.5",
                GST="4.5",
                WVHT=None,
                DPD=None,
                APD=None,
                MWD=None,
                PRES="1013.5",
                ATMP="24.9",
                WTMP="26.5",
                DEWP=None,
                VIS=None,
                PTDY=None,
                TIDE=None,
            ),
            buoys.RawWeatherRecord(
                YY="2022",
                MM="09",
                DD="04",
                hh="18",
                mm="00",
                WDIR="183",
                WSPD="3.6",
                GST="4.9",
                WVHT=None,
                DPD=None,
                APD=None,
                MWD=None,
                PRES="1013.6",
                ATMP="25.3",
                WTMP="26.5",
                DEWP=None,
                VIS=None,
                PTDY=None,
                TIDE=None,
            ),
        ]
    )
    input_weather_report = "\n".join(mock_ndbc_weather_report.splitlines()[:4])
    assert (
        buoys.RawWeatherReport.from_raw_report(input_weather_report) == expected_report
    )
