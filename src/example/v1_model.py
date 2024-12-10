from flask import Flask, request
import os
import requests

app = Flask(__name__)

class ConversationFlowStatus:
    WaitingForContactInfo = "WaitingForContactInfo"
    WaitingForContactLocation = "WaitingForContactLocation"
    WaitingForFinish = "WaitingForFinish"

user_conversations = {}

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def send_message(to, message, phone_number_id):
    url = f"https://graph.facebook.com/v16.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Failed to send message to {to}. Response: {response.status_code} {response.text}")
    else:
        print(f"Message sent to {to}.")

@app.route("/", methods=["GET"])
def home():
    return "API is up", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.get_json()
    if data:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                phone_number_id = value.get("metadata", {}).get("phone_number_id")
                message_data = value.get("messages", [])
                for message in message_data:
                    handle_message(message, phone_number_id)
    return "EVENT_RECEIVED", 200

def handle_message(message, phone_number_id):
    sender_id = message["from"]
    text = message.get("text", {}).get("body", "").strip().lower()

    if sender_id not in user_conversations:
        user_conversations[sender_id] = ConversationFlowStatus.WaitingForContactInfo

    current_status = user_conversations[sender_id]

    if text == "/start" and current_status == ConversationFlowStatus.WaitingForContactInfo:
        send_message(sender_id, "To start, we need your contact info. Please share your contact.", phone_number_id)
        user_conversations[sender_id] = ConversationFlowStatus.WaitingForContactInfo

    elif current_status == ConversationFlowStatus.WaitingForContactInfo:
        if text.startswith("send contact"):
            send_message(sender_id, "Great! Now we need your location. Please share it.", phone_number_id)
            user_conversations[sender_id] = ConversationFlowStatus.WaitingForContactLocation
        else:
            send_message(sender_id, "Please send your contact info to proceed.", phone_number_id)

    elif current_status == ConversationFlowStatus.WaitingForContactLocation:
        if text.startswith("send location"):
            send_message(sender_id, "Ok! Now, finish by sending /finish.", phone_number_id)
            user_conversations[sender_id] = ConversationFlowStatus.WaitingForFinish
        else:
            send_message(sender_id, "Please share your location to proceed.", phone_number_id)

    elif current_status == ConversationFlowStatus.WaitingForFinish:
        if text == "/finish":
            send_message(sender_id, "Thank you! The process is complete.", phone_number_id)
            del user_conversations[sender_id]
        else:
            send_message(sender_id, "Send /finish to complete the process.", phone_number_id)
    else:
        send_message(sender_id, "Invalid input. Please start over by sending /start.", phone_number_id)

if __name__ == "__main__":
    app.run(port=5000)
