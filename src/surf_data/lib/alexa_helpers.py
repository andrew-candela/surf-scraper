from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ask_sdk_model.slot import Slot


def resolve_canonical_value(intent_slot: "Slot") -> str:
    """
    Pulls the canonical value out of the slot payload.
    We'll have to traverse the "resolutions" key.
    """
    resolutions = intent_slot.resolutions.resolutions_per_authority
    matched_resolutions = [res for res in resolutions if res.status.code.value == "ER_SUCCESS_MATCH"]
    res = matched_resolutions[0]
    return res.values[0].value.name