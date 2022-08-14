from ask_sdk_core.dispatch_components import AbstractRequestHandler
import ask_sdk_core.utils as ask_utils
from surf_data.log_entry import LogEntry, prepare_and_submit_entry
from surf_data.lib.time_helpers import map_time_to_datetime
from surf_data.lib.alexa_helpers import resolve_canonical_value, prepare_log_entry_farewell

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ask_sdk_model import Response
    from ask_sdk_core.handler_input import HandlerInput
        

class LogEntryHandler(AbstractRequestHandler):
    """Handler for LogEntry Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            ask_utils.is_intent_name("log_entry")(handler_input)
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        spot = resolve_canonical_value(slots['surf_spot'])
        entry_datetime = map_time_to_datetime(slots['entry_datetime'].value)
        notes = slots['notes'].value
        rating = slots['rating'].value
        entry = LogEntry(entry_date=entry_datetime, spot_name=spot, rating=rating, notes=notes)
        prepare_and_submit_entry(entry)
        speak_output = f"""
            <speak>
                I've logged the entry for {spot}.
                {prepare_log_entry_farewell(rating, notes)}
            </speak>
        """

        return (
            handler_input.response_builder
                         .speak(speak_output)
                         .response
        )