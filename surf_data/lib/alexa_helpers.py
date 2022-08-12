from random import choice
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ask_sdk_model.slot import Slot


SPOT_CHECK_FAREWELLS = (
    "Now get out there and have fun!",
    "<emphasis level=\"moderate\">Now go have fun you kook!</emphasis>",
    "Hope you have a good time out there!",
    "Good luck and have fun!",
    "Go get 'em you kook.",
    "Now go splash around in the ocean you big kook.",
)


def resolve_canonical_value(intent_slot: "Slot") -> str:
    """
    Pulls the canonical value out of the slot payload.
    We'll have to traverse the "resolutions" key.
    """
    resolutions = intent_slot.resolutions.resolutions_per_authority
    matched_resolutions = [res for res in resolutions if res.status.code.value == "ER_SUCCESS_MATCH"]
    res = matched_resolutions[0]
    return res.values[0].value.name

def prepare_spot_check_farewell() -> str:
    return choice(SPOT_CHECK_FAREWELLS)

def prepare_log_entry_farewell(rating: str, notes: str) -> str:
    if " fun " in notes:
        return "Glad you got to have some fun."
    if rating in ("fair", "good", "great"):
        return "Sounds like you had a good time!"
    else:
        return choice((
            "Sounds rough. Did you at least maybe see some fish?",
            "Sounds tough. At least it was good exercise right?",
        ))