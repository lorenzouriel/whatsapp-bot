# WhatsApp Bot Initial Template

## Requirements

- Python 3.12+
- Flask
- dotenv
- requests
- ngrok (for webhook testing)

## Setup

### 1. Environment Variables

Create a `.env` file in the project root with the following content:

```env
VERIFY_TOKEN=*****
ACCESS_TOKEN=*****
PHONE_NUMBER_ID=*****
PHONE_NUMBER=*****
```

### 2. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt

pip install flask python-dotenv requests
```

### 3. Running the Webhook
Start the Flask application:
```bash
python .\src\run.py
```

Expose the application using ngrok:
```bash
ngrok http 5000
```

Copy the forwarding URL (e.g., `https://<ngrok-url>.ngrok-free.app`) and use it to configure the webhook in WhatsApp Business Manager.

### 4. Configure your Webhook on Meta Developers Site
To receive alerts when a message arrives or when the status of a message changes, you need to configure a Webhooks endpoint for your application. [Learn how to configure Webhooks](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started#configure-webhooks).

### 5. Testing Message Sending
Open Whatsapp and start the chat.