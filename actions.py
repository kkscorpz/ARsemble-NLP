from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Sample database
motherboards = {
    "gigabyte h610m k ddr4": {
        "name": "GIGABYTE H610M K DDR4",
        "socket": "LGA1700",
        "chipset": "Intel H610",
        "ram": "DDR4 up to 64GB",
        "price": "₱4,500"
    },
    "msi b450m-a pro max ii": {
        "name": "MSI B450M-A PRO MAX II",
        "socket": "AM4",
        "chipset": "AMD B450",
        "ram": "DDR4 up to 64GB",
        "price": "₱3,900"
    }
}

class ActionBoardDetails(Action):
    def name(self) -> Text:
        return "action_board_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        board = next(tracker.get_latest_entity_values("motherboard"), None)
        if board:
            key = board.lower().strip()
            if key in motherboards:
                details = motherboards[key]
                dispatcher.utter_message(
                    text=f"Here are the details for **{details['name']}**:\n"
                         f"- Socket: {details['socket']}\n"
                         f"- Chipset: {details['chipset']}\n"
                         f"- RAM: {details['ram']}\n"
                         f"- Price: {details['price']}"
                )
            else:
                dispatcher.utter_message(text=f"Sorry, I don’t have details for **{board}**. I only know about GIGABYTE H610M K DDR4 or MSI B450M-A PRO MAX II.")
        else:
            dispatcher.utter_message(text="Please specify which motherboard you want details for.")

        return []


class ActionFindMotherboard(Action):
    def name(self) -> Text:
        return "action_find_motherboard"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I can provide details for specific boards like GIGABYTE H610M K DDR4 or MSI B450M-A PRO MAX II. What would you like to know?")
        return [] 


class ActionCompareBoards(Action):
    def name(self) -> Text:
        return "action_compare_boards"

    def run(self, dispatcher, tracker, domain):
        entities = list(tracker.get_latest_entity_values("motherboard"))
        if len(entities) >= 2:
            b1, b2 = entities[0].lower().strip(), entities[1].lower().strip()
            if b1 in motherboards and b2 in motherboards:
                d1, d2 = motherboards[b1], motherboards[b2]
                msg = (f"**Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| Socket | {d1['socket']} | {d2['socket']} |\n"
                       f"| Chipset | {d1['chipset']} | {d2['chipset']} |\n"
                       f"| RAM | {d1['ram']} | {d2['ram']} |\n"
                       f"| Price | {d1['price']} | {d2['price']} |") 
                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(text="One or both of the boards are not in my database.")
        else:
            dispatcher.utter_message(text="Please mention two motherboards to compare.")

        return []


class ActionPriceCheck(Action):
    def name(self) -> Text:
        return "action_price_check"

    def run(self, dispatcher, tracker, domain):
        board = next(tracker.get_latest_entity_values("motherboard"), None)
        if board:
            key = board.lower().strip()
            if key in motherboards:
                price = motherboards[key]["price"]
                dispatcher.utter_message(text=f"The price of **{motherboards[key]['name']}** is **{price}**.")
            else:
                dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{board}**.")
        else:
            dispatcher.utter_message(text="Please tell me which motherboard you want the price for.")

        return []

# Removed ActionMotherboardDetails