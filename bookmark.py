import requests
import os
import argparse
from datetime import datetime
from dotenv import load_dotenv  # dotenvをインポート
from pathlib import Path
env_path = Path('.') / '.env'
# .envファイルを読み込む
load_dotenv()

# 環境変数からトークンとデータベースIDを取得
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")  # .envから取得
NOTION_API_URL = os.getenv("NOTION_API_URL")

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description='Notionに新しいエントリーを追加します。')
parser.add_argument('entry', type=str, help='タイトルとURLをカンマで区切ったエントリー')

# 引数を解析
args = parser.parse_args()

# タイトルとURLをカンマで分割
entry_parts = args.entry.split(',')
if len(entry_parts) != 2:
    print("エラー: タイトルとURLをカンマで区切って入力してください。")
    exit(1)

title = entry_parts[0]
url = entry_parts[1]

# APIリクエストヘッダー
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  # 適切なバージョンを指定
}

# 今日の日付を取得
today_date = datetime.today().strftime('%Y-%m-%d')

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
        "status": {  # Statusプロパティを追加
            "status": {
                "name": "未着手"
            }
        },
        "date": {  # Dateプロパティを追加
            "date": {
                "start": today_date  # 今日の日付
            }
        }
    }
}
if not NOTION_API_URL:
    raise ValueError("NOTIONAPI_URL が設定されていません。'.env' ファイルを確認してください。")

# APIリクエスト送信
response = requests.post(NOTION_API_URL, headers=headers, json=payload)

# 結果を簡素に表示
if response.status_code == 200:
    print("complete!")
else:
    print(f"Error: {response.status_code}")

