from flask import Flask, render_template_string
import requests
app = Flask(__name__)
token = None
mai = None
pas = None
@app.route('/login')
def index():
  mai = request.args.get('m')
  pas = request.args.get('p')
  url = "https://api.revolt.chat/auth/session/login"
　payload = {"email": mai,"password": pas}
　headers = {"Content-Type": "application/json","X-Session-Token": "YOUR_TOKEN"}
　response = requests.patch(url, json=payload, headers=headers)
  token = data['token']
  return "Login"

@app.route('/ch')
def index2():
    # チャンネルIDとAPIトークンを設定
    channel_id = request.args.get('id')  # チャンネルのIDを入力
    url = f'https://api.revolt.chat/channels/{channel_id}/messages'
    headers = {
        'Authorization': f'{token}'  # APIトークンを入力
    }

    # メッセージを取得
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        messages = response.json()

        # メッセージを格納するリスト
        formatted_messages = []

        # 最初の10件を取得してフォーマット
        for msg in messages[:10]:
            username = msg['author']['username']
            content = msg['content']
            formatted_messages.append(f"{username}: {content}")

        # 変数にまとめたメッセージをHTMLで表示
        result = "<br>".join(formatted_messages)
    else:
        result = f"Error: {response.status_code}"

    # HTMLテンプレートを作成
    html_template = '''
    <!doctype html>
    <html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>Revolt Messages</title>
    </head>
    <body>
        <h1>メッセージ一覧</h1>
        <div>{{ messages|safe }}</div>
    </body>
    </html>
    '''

    return render_template_string(html_template, messages=result)
if __name__ == '__main__':
    app.run(debug=True)
