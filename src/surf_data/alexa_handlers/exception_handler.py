

from ask_sdk_core.dispatch_components import AbstractExceptionHandler

import logging
import typing
if typing.TYPE_CHECKING:
    from ask_sdk_model import Response
    from ask_sdk_core.handler_input import HandlerInput


logger = logging.getLogger(__name__)


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors.
    If you receive an error stating the request handler chain is not found,
    you have not implemented a handler for the intent being invoked
    or included it in the skill builder.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. " \
                       "Please try again. Oh, I mean go home kook!"

        return (
            handler_input.response_builder
                         .speak(speak_output)
                         .ask(speak_output)
                         .response
        )