import requests
import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# .envファイルの読み込み
env_path = Path('.') / '.env'
load_dotenv()

# 環境変数の取得
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
NOTION_API_URL = os.getenv("NOTION_API_URL")

if not NOTION_TOKEN or not DATABASE_ID or not NOTION_API_URL:
    raise ValueError(".envファイルの設定を確認してください。NOTION_TOKEN, DATABASE_ID, NOTION_API_URLが必要です。")

# 引数を再結合
if len(sys.argv) < 2:
    print("エラー: タイトルとURLをカンマで区切って入力してください。例: タイトル,URL")
    sys.exit(1)

# コマンドライン引数を結合
entry = " ".join(sys.argv[1:])  # 全ての引数をスペースで結合
entry_parts = re.split(r'[，,]', entry, maxsplit=1)  # 半角カンマ・全角カンマで分割

if len(entry_parts) != 2:
    print("エラー: タイトルとURLをカンマで区切って入力してください。例: タイトル,URL")
    sys.exit(1)

title = entry_parts[0].strip()
url = entry_parts[1].strip()

# APIリクエストのヘッダー
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  
}

# 今日の日付を取得
today_date = datetime.today().strftime('%Y-%m-%d')

# リクエストペイロードの構築
payload = {
    "parent": {
        "database_id": DATABASE_ID
    },
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "URL": {
            "url": url
        },
        "status": {
            "status": {
                "name": "未着手"
            }
        },
        "date": {
            "date": {
                "start": today_date
            }
        }
    }
}

# APIリクエスト送信
response = requests.post(NOTION_API_URL, headers=headers, json=payload)

# 結果を表示
if response.status_code == 200:
    print("complete!")
else:
    print(f"Error: {response.status_code}, {response.text}")
