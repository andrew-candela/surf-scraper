from dataclasses import dataclass, asdict
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional
from surf_data.lib.buoys import ConditionReport
from surf_data.lib.tides import TideData
from surf_data.lib.dynamo import SurfDiaryDB, DDB_DATE_FORMAT
from surf_data.get_data import get_spot_data
import asyncio


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="{levelname}:: {asctime}:: {filename}:: {message}",
    style="{",
)


@dataclass
class LogEntry:
    entry_date: datetime
    spot_name: str
    rating: str
    notes: str
    wind_and_waves: Optional[ConditionReport] = None
    tides: Optional[TideData] = None

    def serialize_for_database(self) -> Dict[str, Any]:
        return {
            "Item": dict(
                entry_date=self.entry_date.strftime(DDB_DATE_FORMAT),
                spot_name=self.spot_name,
                rating=self.rating,
                notes=self.notes,
                **asdict(self.wind_and_waves),
                **asdict(self.tides),
            )
        }


def prepare_and_submit_entry(entry_data: LogEntry) -> None:
    """
    Takes a LogEntry object prepared by the Alexa handler.
    Gathers tide and wave data and submits the log entry to the database.
    """
    logging.info("Grabbing external data...")
    conditions, tide = asyncio.run(
        get_spot_data(entry_data.spot_name, entry_data.entry_date)
    )
    entry_data.wind_and_waves = conditions
    entry_data.tides = tide
    db = SurfDiaryDB()
    logging.info("persisting entry to the DB...")
    db.persist_entry(args=entry_data.serialize_for_database())
    logging.info(f"All done!")


def get_latest_entry(spot):
    db = SurfDiaryDB()
    latest_entry = db.get_latest_entry(spot)
    logging.info(f"{latest_entry=}")


if __name__ == "__main__":
    from surf_data import Spots

    # main({}, {})
    # get_latest_entry(Spots.montara.value)
    entry = LogEntry(
        entry_date=datetime(2022, 9, 10, 17),
        spot_name=Spots.montara.value,
        rating="fair",
        notes="Strong northward current. Discrete points where waves broke well. Good conditions.",
    )
    prepare_and_submit_entry(entry)
