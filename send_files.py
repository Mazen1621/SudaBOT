import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def send_document(file_path, caption=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, 'rb') as f:
        files = {'document': f}
        data = {'chat_id': CHAT_ID}
        if caption:
            data['caption'] = caption
        response = requests.post(url, data=data, files=files)
        return response.json()

def main():
    # Send source code zip
    print("Sending source code zip...")
    result1 = send_document('scholarship_bot_source.zip', caption='Scholarship Bot Source Code')
    print("Zip send result:", result1.get('ok'))
    
    # Send guide as txt
    print("Sending guide...")
    result2 = send_document('GUIDE.txt', caption='GitHub Setup and Automation Guide')
    print("Guide send result:", result2.get('ok'))
    
    if result1.get('ok') and result2.get('ok'):
        print("Both files sent successfully!")
    else:
        print("Some files failed to send.")

if __name__ == '__main__':
    main()
