import os
import requests

def send_document():
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    if not bot_token or not chat_id:
        print("Error: BOT_TOKEN and CHAT_ID must be set in environment")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    with open('scholarship_bot_source.zip', 'rb') as f:
        files = {'document': f}
        data = {'chat_id': chat_id}
        response = requests.post(url, data=data, files=files)
        result = response.json()
        if result.get('ok'):
            print("Document sent successfully")
            return True
        else:
            print(f"Failed to send document: {result.get('description')}")
            return False

if __name__ == '__main__':
    send_document()
