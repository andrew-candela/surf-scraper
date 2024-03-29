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

GREETINGS = (
    (
        "<amazon:emotion name=\"excited\" intensity=\"medium\">Hey, surf's up bro!</amazon:emotion> "
        "I'm just kidding, I don't know if the surf is up. But I can check for you!"
    ),
    "Welcome to the Surf Log. Did you want to tell me about a surf?",
    (
        "Welcome to Surf Log. I want to hear about your surfing! "
        "Keep in mind I don't actually care because I'm not alive."
    ),
    "Hi Andrew!",
    (
        "<amazon:emotion name=\"excited\" intensity=\"low\">"
        "Hey bro, you getting ready to go shred the gnar?</amazon:emotion> "
        "That's something surfers say... right?"
    )
)


def resolve_canonical_value(intent_slot: "Slot") -> str:
    """
    Pulls the canonical value out of the slot payload.
    We'll have to traverse the "resolutions" key.
    """
    resolutions = intent_slot.resolutions.resolutions_per_authority
    matched_resolutions = [
        res for res in resolutions
        if res.status.code is not None
        and res.status.code.value == "ER_SUCCESS_MATCH"
    ]
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

def prepare_greeting():
    return choice(GREETINGS)
