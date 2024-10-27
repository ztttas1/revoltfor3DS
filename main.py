from flask import Flask, request, jsonify
import requests
import json
app = Flask(__name__)

# グローバル変数としてtokenを保存
token = None

@app.route('/login', methods=['GET'])
def login():
    global token
    m = request.args.get('m')
    p = request.args.get('p')

    url = "https://api.revolt.chat/auth/session/login"
    payload = {"email": m, "password": p}
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get('token')
        return jsonify({'status': 'success', 'token': token})
    else:
        return jsonify({'status': 'error', 'message': response.text}), response.status_code

@app.route('/', methods=['GET'])
def get_messages():
    global token
    channel_id = request.args.get('channel_id')

    if not token:
        return jsonify({'status': 'error', 'message': 'Not authenticated. Please log in first.'}), 401

    url = f"https://api.revolt.chat/channels/{channel_id}/messages"
    headers = {"X-Session-Token": token}

    response = requests.get(url, headers=headers)

    print(f"Requesting messages from channel {channel_id} with token {token}")  # デバッグ用
    json_load = json.load(response)
    if response.status_code == 200:
        messages = response.json()

        # ここでmessagesの内容を印刷して確認
        print("Response messages:", messages)

        # messagesがリストであることを確認
        if isinstance(messages, list):
            formatted_messages = [
                {'username': json_load['users'], 'content': json_load['messages']}
                for msg in messages
            ]
            return jsonify(formatted_messages)
        else:
            return jsonify({'status': 'error', 'message': 'Unexpected response format. Expected a list.'}), 500
    else:
        error_message = response.text
        return jsonify({'status': 'error', 'message': error_message}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
