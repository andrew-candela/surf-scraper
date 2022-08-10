"""
This is mostly boilerplate alexa skill code.
We set up the skill builder object and then add
the intent handlers.
"""


from ask_sdk_core.skill_builder import SkillBuilder
from surf_data import alexa_handlers

# The SkillBuilder object acts as the entry point for your skill,
# routing all request and response payloads to the handlers above.
# Make sure any new handlers or interceptors you've defined are included below.
# The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(alexa_handlers.LaunchRequestHandler())
sb.add_request_handler(alexa_handlers.GetConditionsHandler())
sb.add_request_handler(alexa_handlers.LogEntryHandler())
sb.add_request_handler(alexa_handlers.HelpIntentHandler())
sb.add_request_handler(alexa_handlers.CancelOrStopIntentHandler())
sb.add_request_handler(alexa_handlers.SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't
# override your custom intent handlers
sb.add_request_handler(alexa_handlers.IntentReflectorHandler())
sb.add_exception_handler(alexa_handlers.CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()