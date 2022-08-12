import asyncio
from ask_sdk_core.dispatch_components import AbstractRequestHandler
import ask_sdk_core.utils as ask_utils
from surf_data.lib.alexa_helpers import resolve_canonical_value, prepare_spot_check_farewell
from surf_data.get_data import get_spot_data

import typing
if typing.TYPE_CHECKING:
    from ask_sdk_model import Response
    from ask_sdk_core.handler_input import HandlerInput


def prepare_spot_condition_report(spot: str) -> str:
    """
    grabs wave and tide data and pops them into a string for
    Alexa to speak.
    """
    wave, tide = asyncio.run(get_spot_data(spot))
    return (
        f"Here's your report for {spot}. "
        f"{tide.serialize_for_alexa()} "
        f"{wave.serialize_for_alexa()} "
        f"{prepare_spot_check_farewell()}"
    )



class GetConditionsHandler(AbstractRequestHandler):
    """
    Used for grabbing tide and wave conditions for a certain spot
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print(f"You are trying to call can_handle from {__name__}")
        return ask_utils.is_intent_name("get_conditions")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        spot = resolve_canonical_value(slots['surf_spot'])
        
        output = prepare_spot_condition_report(spot)

        return (
            handler_input.response_builder
                         .speak(output)
                         .response
        )
