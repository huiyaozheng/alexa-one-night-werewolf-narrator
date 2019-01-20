# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

SKILL_NAME = "One night werewolf"
GET_FACT_MESSAGE = "Here's your fact: "
HELP_MESSAGE = "You can say start a game with some number of people, or, you can say check the configuration for some number of people. What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "I am not expecting to trigger the fallback function."
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."

narration = {
    "start" : "Everyone, close your eyes.";
    "wolves_1" : "Werewolves, wake up and look for other werewolves. If there is only one werewolf, you may look at a card from the centre.";
    "wolves_2" : "Werewolves, close your eyes.";
    "mystic_wolf_1" : "Mystic wolf, if you did not look at a card from the centre just now, you can wake up and do so.";
    "mystic_wolf_2" : "Mystic wolf, close your eyes.";
    "minion_1" : "Minion, wake up. Werewolves, stick out your thumb so the minion can see who you are.";
    "minion_2" : "Werewolves, put your thumb away. Minion, close your eyes.";
    "seer_1" : "Seer, wake up. You may look at another player's card or two of the centre cards.";
    "seer_2" : "Seer, close your eyes.";
    "apprentice_seer_1" : "Apprentice seer, wake up. You may look at one of the centre cards.";
    "apprentice_seer_2" : "Apprentice seer, close your eyes.";
    "pi_1" : "Paranormal investigator, wake up. You may look at up to two cards of other players. However, if you see a wolf, you become a wolf for this game and stop your action.";
    "pi_2" : "Paranormal investigator, close your eyes.";
    "robber_1" : "Robber, wake up. You must exchange your card with another player's card, and then view your new card.";
    "robber_2" : "Robber, close your eyes.";
    "troublemaker_1" : "Troublemaker, wake up. You may exchange cards between two other players.";
    "troublemake_2" : "Troublemaker, close your eyes.";
    "village_idiot_1" : "Village idiot, wake up. You may move everyone's card except your own to the left or to the right.";
    "village_idiot_2" : "Village idiot, close your eyes.";
    "drunk_1" : "Drunk, wake up and exchange your card with a card in the centre.";
    "drunk_2" : "Drunk, close your eyes.";
    "insomniac_1" : "Insomniac, wake up and have a look at your card.";
    "insomniac_2" : "Insomniac, close your eyes.";
    "end" : "Everyone, keep your eyes closed and reach out and move your card around slightly. Everyone, wake up!"
}

card_definitions = {
    "wolves" : "black aces";
    "mystic wolf" : "ace of spade";
    "minion" : "a black two";
    "seer" : "a red seven";
    "apprentice seer" : "a red five";
    "paranormal investigator" : "joker";
    "robber" : "a red jack";
    "trouble maker" : "a red queen";
    "drunk" : "a red ten";
    "insomniac" : "a red nine";
    "tanner" : "a black four";
    "village idiot" : "a red five";
    "villagers" : "red threes"
}

configurations = {
    6 : [{"name" : "wolves"; "quantity" : 1}, 
         {"name" : "mystic wolf"; "quantity" : 1},
         {"name" : "minion"; "quantity" : 1},
         {"name" : "seer"; "quantity" : 1},
         {"name" : "apprentice seer"; "quantity" : 1}, 
         {"name" : "robber"; "quantity" : 1},
         {"name" : "troublemaker"; "quantity" : 1},
         {"name" : "drunk"; "quantity" : 1},
         {"name" : "insomniac"; "quantity" : 1}];
    7 : [{"name" : "wolves"; "quantity" : 1}, 
         {"name" : "mystic wolf"; "quantity" : 1},
         {"name" : "minion"; "quantity" : 1},
         {"name" : "seer"; "quantity" : 1},
         {"name" : "apprentice seer"; "quantity" : 1}, 
         {"name" : "robber"; "quantity" : 1},
         {"name" : "troublemaker"; "quantity" : 1},
         {"name" : "drunk"; "quantity" : 1},
         {"name" : "insomniac"; "quantity" : 1},
         {"name" : "villager"; "quantity" : 1}];
    8 : [{"name" : "wolves"; "quantity" : 1}, 
         {"name" : "mystic wolf"; "quantity" : 1},
         {"name" : "minion"; "quantity" : 1},
         {"name" : "seer"; "quantity" : 1},
         {"name" : "apprentice seer"; "quantity" : 1}, 
         {"name" : "paranormal investigator"; "quantity" : 1}, 
         {"name" : "robber"; "quantity" : 1},
         {"name" : "troublemaker"; "quantity" : 1},
         {"name" : "drunk"; "quantity" : 1},
         {"name" : "insomniac"; "quantity" : 1},
         {"name" : "villager"; "quantity" : 1}];
    9 : [{"name" : "wolves"; "quantity" : 1}, 
         {"name" : "mystic wolf"; "quantity" : 1},
         {"name" : "minion"; "quantity" : 1},
         {"name" : "seer"; "quantity" : 1},
         {"name" : "apprentice seer"; "quantity" : 1}, 
         {"name" : "paranormal investigator"; "quantity" : 1}, 
         {"name" : "robber"; "quantity" : 1},
         {"name" : "troublemaker"; "quantity" : 1},
         {"name" : "drunk"; "quantity" : 1},
         {"name" : "insomniac"; "quantity" : 1},
         {"name" : "villager"; "quantity" : 2}];
    10 : [{"name" : "wolves"; "quantity" : 1}, 
         {"name" : "mystic wolf"; "quantity" : 1},
         {"name" : "minion"; "quantity" : 1},
         {"name" : "seer"; "quantity" : 1},
         {"name" : "apprentice seer"; "quantity" : 1}, 
         {"name" : "paranormal investigator"; "quantity" : 1}, 
         {"name" : "robber"; "quantity" : 1},
         {"name" : "troublemaker"; "quantity" : 1},
         {"name" : "drunk"; "quantity" : 1},
         {"name" : "insomniac"; "quantity" : 1},
         {"name" : "tanner"; "quantity" : 1},
         {"name" : "villager"; "quantity" : 2}];
    11 : [{"name" : "wolves"; "quantity" : 1}, 
         {"name" : "mystic wolf"; "quantity" : 1},
         {"name" : "minion"; "quantity" : 1},
         {"name" : "seer"; "quantity" : 1},
         {"name" : "apprentice seer"; "quantity" : 1}, 
         {"name" : "paranormal investigator"; "quantity" : 1}, 
         {"name" : "robber"; "quantity" : 1},
         {"name" : "troublemaker"; "quantity" : 1},
         {"name" : "drunk"; "quantity" : 1},
         {"name" : "insomniac"; "quantity" : 1},
         {"name" : "tanner"; "quantity" : 1},
         {"name" : "village idiot"; "quantity" : 1},
         {"name" : "villager"; "quantity" : 2}];
    12 : [{"name" : "wolves"; "quantity" : 1}, 
         {"name" : "mystic wolf"; "quantity" : 1},
         {"name" : "minion"; "quantity" : 1},
         {"name" : "seer"; "quantity" : 1},
         {"name" : "apprentice seer"; "quantity" : 1}, 
         {"name" : "paranormal investigator"; "quantity" : 1}, 
         {"name" : "robber"; "quantity" : 1},
         {"name" : "troublemaker"; "quantity" : 1},
         {"name" : "drunk"; "quantity" : 1},
         {"name" : "insomniac"; "quantity" : 1},
         {"name" : "tanner"; "quantity" : 1},
         {"name" : "village idiot"; "quantity" : 1},
         {"name" : "villager"; "quantity" : 3}];
}

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class StartAWerewolfGameHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("StartAWerewolfGame")(handler_input)

    def handle(self, handler_input):
        logger.info("In StartAWerewolfGameHandler")
        slots = handler_input.request_envelope.request.intent.slots
        player_number = int(slots["playerNumber"].value)
        if 6 <= player_number <=12:
            configuration = configurations[player_number]
        else:



# Built-in Intent Handlers
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
