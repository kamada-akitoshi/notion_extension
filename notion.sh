#!/bin/bash

# スクリプトのディレクトリを取得
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# コマンド引数をチェック
COMMAND=$1
shift  # 最初の引数 (コマンド) を削除して残りを渡す

case "$COMMAND" in
  bookmark)
    python3 "$SCRIPT_DIR/bookmark.py" "$@"
    ;;
  another)
    python3 "$SCRIPT_DIR/another_feature.py" "$@"
    ;;
  *)
    echo "Usage: notion {bk|another} [arguments]"
    ;;
esac
