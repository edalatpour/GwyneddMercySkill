# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
from datetime import date

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

import CalendarUtil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

schoolCalendarUri = "https://www.gmaelem.org/calendar/calendar_242.ics"
menuCalendarUri = "https://www.gmaelem.org/calendar/calendar_298.ics"
athleticCalendarUri = "https://www.gmaelem.org/calendar/page_534.ics"

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask me about the events on any date. For example, say 'Events on Tuesday'"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
def ProcessRequest(handler_input, caption, calendarUri):

    request_date = date.today()
        
    slots = handler_input.request_envelope.request.intent.slots
    date_slot = slots["date"]
    request_date = date_slot.value
            
    items = CalendarUtil.GetItemsForDate(request_date, caption, calendarUri, logger)

    response = ""
    card_text = ""
    card_title = "{0} on {1}".format(caption, request_date)
    

    count = len(items)
    
    logger.info("EventsIntentHandler: Calendar returned {0} items.".format(count))

    if count == 0:
        response = "I didn't find any items on the {0} on {1}. You can say another day to search again.".format(caption.lower(),request_date)
    else:

        intro = ""

        if count == 1:
            intro = "I found one item on"
        else:
            intro = "I found {0} items on".format(count)

        index = 0
        eventText = ""
        for item in items:
            index = index + 1
            eventText = eventText + "{0}. {1}.\n".format(index, item)

        response = "{0} the {1} on {2}.\n\n{3}\nYou can say another day to search again.".format(intro, caption.lower(), request_date, eventText)
    
        card_text = eventText

    speech_text = response

    return (
        handler_input.response_builder
        .speak(speech_text)
        .set_card(SimpleCard(card_title, card_text))
        .ask("You can say another day to search again. Or say events, menu, or sports.")
        .response
    )

class EventsIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("EventsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return(ProcessRequest(handler_input, "School Calendar", schoolCalendarUri))
        

class MenuIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MenuIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return(ProcessRequest(handler_input, "Menu", menuCalendarUri))
        

class SportsIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SportsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return(ProcessRequest(handler_input, "Athletic Calendar", athleticCalendarUri))
        

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "I can tell you the events, menu or sports for any day on the calendar. For example, you can say 'Events on Tuesday', 'Menu today', or 'Sports on November Second'."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        #speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        speak_output = exception.to_string()

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(EventsIntentHandler())
sb.add_request_handler(MenuIntentHandler())
sb.add_request_handler(SportsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()