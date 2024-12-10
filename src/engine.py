# conversation.py
from send_message import send_message

class ConversationFlowStatus:
    WaitingContact = "WaitingContact"
    WaitingLocation = "WaitingLocation"
    WaitingFinish = "WaitingFinish"

user_conversations = {}

def handle_message(message, phone_number_id):
    sender_id = message["from"]
    text = message.get("text", {}).get("body", "").strip().lower()

    if sender_id not in user_conversations:
        user_conversations[sender_id] = ConversationFlowStatus.WaitingContact

    current_status = user_conversations[sender_id]

    if text == "/start" and current_status == ConversationFlowStatus.WaitingContact:
        send_message(sender_id, "To start, we need your contact info. Please share your contact.", phone_number_id)
        user_conversations[sender_id] = ConversationFlowStatus.WaitingContact

    elif current_status == ConversationFlowStatus.WaitingContact:
        if text.startswith("send contact"):
            send_message(sender_id, "Great! Now we need your location. Please share it.", phone_number_id)
            user_conversations[sender_id] = ConversationFlowStatus.WaitingLocation
        else:
            send_message(sender_id, "Please send your contact info to proceed.", phone_number_id)

    elif current_status == ConversationFlowStatus.WaitingLocation:
        if text.startswith("send location"):
            send_message(sender_id, "Ok! Now, finish by sending /finish.", phone_number_id)
            user_conversations[sender_id] = ConversationFlowStatus.WaitingFinish
        else:
            send_message(sender_id, "Please share your location to proceed.", phone_number_id)

    elif current_status == ConversationFlowStatus.WaitingFinish:
        if text == "/finish":
            send_message(sender_id, "Thank you! The process is complete.", phone_number_id)
            del user_conversations[sender_id]
        else:
            send_message(sender_id, "Send /finish to complete the process.", phone_number_id)
    else:
        send_message(sender_id, "Invalid input. Please start over by sending /start.", phone_number_id)
