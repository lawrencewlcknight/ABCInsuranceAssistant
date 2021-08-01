# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import json
from typing import Any, Text, Dict, List
import logging

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet
)

from rasa_sdk.forms import FormValidationAction

logger = logging.getLogger(__name__)

MOCK_DATA = json.load(open("actions/mock_data.json", "r"))

# Get New Quote Actions

class ActionGetQuote(Action):
    """Gets an insurance quote"""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "action_get_quote"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        slots = ["AGE", "LICENCE_YEARS"]

        # Build the quote from the provided data.
        AGE = int(tracker.get_slot("AGE"))
        LICENCE_YEARS = int(tracker.get_slot("LICENCE_YEARS"))

        final_quote = 500 + (2*abs(AGE - 45)) - (2*LICENCE_YEARS)


        msg_params = {
            "final_quote": final_quote,
            "AGE": int(tracker.get_slot("AGE")),
            "LICENCE_YEARS": int(tracker.get_slot("LICENCE_YEARS"))
        }
        dispatcher.utter_message(template="utter_final_quote", **msg_params)

        # Save the quote details

        # Reset the slot values.
        return [SlotSet(slot, None) for slot in slots]


class ValidateQuoteForm(FormValidationAction):
    """Validates Slots for the Quote form."""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "validate_quote_form"

    def validate_AGE(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validates the age entered is valid."""
        if tracker.get_intent_of_latest_message() == "stop":
            return {"AGE": None}

        try:
            int(value)
        except TypeError:
            dispatcher.utter_message(f"Driver age must be an integer.")
            return {"AGE": None}
        except ValueError:
            dispatcher.utter_message("You must answer with a number.")
            return {"AGE": None}

        if int(value) <= 17:
            dispatcher.utter_message("I'm sorry we don't insure drivers less than 18 years of age.")
            return {"AGE": None}

        if int(value) > 90:
            dispatcher.utter_message("I'm sorry we don't insure drivers older than 90 years of age.")
            return {"AGE": None}

        return {"AGE": value}

    def validate_LICENCE_YEARS(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validates the licence years entered is valid."""
        if tracker.get_intent_of_latest_message() == "stop":
            return {"LICENCE_YEARS": None}

        try:
            int(value)
        except TypeError:
            dispatcher.utter_message(f"Licence years must be an integer.")
            return {"LICENCE_YEARS": None}
        except ValueError:
            dispatcher.utter_message("You must answer with a number.")
            return {"LICENCE_YEARS": None}

        if int(value) < 0:
            dispatcher.utter_message("I'm sorry we can't accept negative licence years values")
            return {"LICENCE_YEARS": None}

        if int(value) > 73:
            dispatcher.utter_message("I'm sorry, based on the figure provided you exceed the maxium age for which we insure drivers")
            return {"LICENCE_YEARS": None}

        return {"LICENCE_YEARS": value}


class ActionStopQuote(Action):
    """Stops quote form and clears collected data."""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "action_stop_quote"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        slots = ["AGE", "LICENCE_YEARS"]

        # Reset the slot values.
        return [SlotSet(slot, None) for slot in slots]

class ValidatePolicyNumberForm(FormValidationAction):
    """Validates Slots for the policy number form."""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "validate_policy_number_form"

    def validate_POLICY_NUMBER(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validates the policy number entered is valid."""
        if tracker.get_intent_of_latest_message() == "stop":
            return {"POLICY_NUMBER": None}

        existing_pol_numbers = [11111111, 99999999]


        try:
            int(value)
        # except TypeError:
        #     dispatcher.utter_message(f"Driver age must be an integer.")
        #     return {"POLICY_NUMBER": None}
        except ValueError:
            dispatcher.utter_message("You must answer with a number.")
            return {"POLICY_NUMBER": None}

        if len(str(value)) < 8:
            dispatcher.utter_message("The policy number should only have eight digits.")
            return {"POLICY_NUMBER": None}

        if len(str(value)) > 8:
            dispatcher.utter_message("The policy number should have eight digits.")
            return {"POLICY_NUMBER": None}

        if int(value) not in existing_pol_numbers:
            dispatcher.utter_message("I'm sorry I don't recognise that policy number.")
            return {"POLICY_NUMBER": None}

        return {"POLICY_NUMBER": value}

class ActionGetCustomerData(Action):

    def name(self) -> Text:
        return "action_get_customer_data"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        
        POLICY_NUMBER = tracker.get_slot("POLICY_NUMBER")
        
        customer_data = {
            "AGE": MOCK_DATA["policy_data"][str(POLICY_NUMBER)]["AGE"],
            "LICENCE_YEARS": MOCK_DATA["policy_data"][str(POLICY_NUMBER)]["LICENCE_YEARS"],
            "FIRST_NAME": MOCK_DATA["policy_data"][str(POLICY_NUMBER)]["FIRST_NAME"],
            "SURNAME_NAME": MOCK_DATA["policy_data"][str(POLICY_NUMBER)]["SURNAME_NAME"],
            "CURRENT_PREMIUM": MOCK_DATA["policy_data"][str(POLICY_NUMBER)]["CURRENT_PREMIUM"]           
        }
        # update slot values
        return [SlotSet(k, v) for k, v in customer_data.items()]

class ActionGetRenewalQuote(Action):
    """Gets a renawal insurance quote"""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "action_get_renewal_quote"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        slots = ["AGE", "LICENCE_YEARS", "CURRENT_PREMIUM"]

        # Build the quote from the provided data.
        AGE = int(tracker.get_slot("AGE"))
        LICENCE_YEARS = int(tracker.get_slot("LICENCE_YEARS"))
        CURRENT_PREMIUM = int(tracker.get_slot("CURRENT_PREMIUM"))

        final_quote = 500 + (2*abs(AGE - 45)) - (2*LICENCE_YEARS)


        msg_params = {
            "final_quote": final_quote,
            "AGE": int(tracker.get_slot("AGE")),
            "LICENCE_YEARS": int(tracker.get_slot("LICENCE_YEARS")),
            "CURRENT_PREMIUM": int(tracker.get_slot("CURRENT_PREMIUM"))
        }

        dispatcher.utter_message(template="utter_renewal_quote", **msg_params)

        # Save the quote details

        return

class ActionResetSlots(Action):
    """Clears all slots"""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "action_reset_slots"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""

        slots = ["AGE", "LICENCE_YEARS", "FIRST_NAME", "SURNAME_NAME", 
        "POLICY_NUMBER", "CURRENT_PREMIUM", "CLAIM_ID", "CLAIM_DATE", 
        "CLAIM_STATUS", "CLAIM_BALANCE"
        ]

        # Reset the slot values.
        return [SlotSet(slot, None) for slot in slots]
  
  
class ValidateClaimIDForm(FormValidationAction):
    """Validates slots for the claim id form."""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "validate_claim_id_form"

    def validate_CLAIM_ID(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validates the claim id entered is valid."""
        if tracker.get_intent_of_latest_message() == "stop":
            return {"CLAIM_ID": None}

        existing_claim_ids = ["AB1234", "AB4321"]

        if len(str(value)) < 6:
            dispatcher.utter_message("The claim id should only have six charatcters.")
            return {"CLAIM_ID": None}

        if len(str(value)) > 6:
            dispatcher.utter_message("The claim id should have six charatcters.")
            return {"CLAIM_ID": None}

        if str(value) not in existing_pol_numbers:
            dispatcher.utter_message("I'm sorry I don't recognise that claim id.")
            return {"CLAIM_ID": None}

        return {"CLAIM_ID": value}


class ActionGetClaimData(Action):

    def name(self) -> Text:
        return "action_get_claim_data"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        
        CLAIM_ID = tracker.get_slot("CLAIM_ID")
        
        claim_data = {
            "CLAIM_DATE": MOCK_DATA["claims_data"][str(CLAIM_ID)]["CLAIM_DATE"],
            "CLAIM_STATUS": MOCK_DATA["claims_data"][str(CLAIM_ID)]["CLAIM_STATUS"],
            "CLAIM_BALANCE": MOCK_DATA["claims_data"][str(CLAIM_ID)]["CLAIM_BALANCE"]
        }
        # update slot values
        return [SlotSet(k, v) for k, v in claim_data.items()]

class ActionGetClaimStatus(Action):
    """Retrieves Claim Status"""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "action_get_claim_status"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        slots = ["CLAIM_DATE", "CLAIM_STATUS", "CLAIM_BALANCE"]

        # Build the quote from the provided data.
        CLAIM_ID = tracker.get_slot("CLAIM_ID")
        CLAIM_DATE = tracker.get_slot("CLAIM_DATE")
        CLAIM_STATUS = tracker.get_slot("CLAIM_STATUS")
        CLAIM_BALANCE = tracker.get_slot("CLAIM_BALANCE")

        msg_params = {
            "CLAIM_ID": CLAIM_ID,
            "CLAIM_DATE": CLAIM_DATE,
            "CLAIM_STATUS": CLAIM_STATUS,
            "CLAIM_BALANCE": CLAIM_BALANCE
        }

        dispatcher.utter_message(template="utter_claim_id_status", **msg_params)

        return
