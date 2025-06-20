#!/bin/bash

# 環境変数設定
export DISPLAY=:0
export HOME=/home/aj

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
GAME_DIR="$(dirname "$SCRIPT_DIR")"

# ログファイルパス
LOG_FILE="$GAME_DIR/logs/game.log"

# ログディレクトリ作成 (念のため最初に実行)
mkdir -p "$GAME_DIR/logs"

echo "=====================================================" >> "$LOG_FILE"
echo "$(date): start_game.sh スクリプト開始" >> "$LOG_FILE"
echo "=====================================================" >> "$LOG_FILE"

cd "$GAME_DIR"
echo "$(date): 現在のディレクトリ: $(pwd)" >> "$LOG_FILE"
echo "$(date): 実行ユーザー: $(whoami)" >> "$LOG_FILE"

# 仮想環境があれば有効化
if [ -d "venv" ]; then
    echo "$(date): Python仮想環境 (venv) を有効化します。" >> "$LOG_FILE"
    source venv/bin/activate
else
    echo "$(date): Python仮想環境 (venv) が見つかりません。" >> "$LOG_FILE"
fi

# --- 自動アップデート処理 ---
echo "$(date): --- 自動アップデート処理開始 ---" >> "$LOG_FILE"

# ネットワーク接続確認 (github.comへのping)
echo "$(date): ネットワーク接続確認中 (ping github.com)..." >> "$LOG_FILE"
ping -c 3 github.com >> "$LOG_FILE" 2>&1
PING_STATUS=$?
if [ $PING_STATUS -ne 0 ]; then
    echo "$(date): github.com へのpingに失敗しました。ステータス: $PING_STATUS。インターネット接続またはDNS解決に問題がある可能性があります。" >> "$LOG_FILE"
    echo "$(date): 今回の自動アップデート処理はスキップします。" >> "$LOG_FILE"
else
    echo "$(date): github.com へのpingに成功しました。" >> "$LOG_FILE"

    echo "$(date): Gitステータス確認中..." >> "$LOG_FILE"
    git status >> "$LOG_FILE" 2>&1

    echo "$(date): 更新チェック中 (git fetch origin main)..." >> "$LOG_FILE"
    git fetch origin main >> "$LOG_FILE" 2>&1
    FETCH_STATUS=$?
    if [ $FETCH_STATUS -ne 0 ]; then
        echo "$(date): git fetch origin main 失敗。ステータス: $FETCH_STATUS" >> "$LOG_FILE"
    else
        echo "$(date): git fetch origin main 成功。" >> "$LOG_FILE"
        LOCAL=$(git rev-parse HEAD)
        REMOTE=$(git rev-parse origin/main)
        echo "$(date): ローカルHEAD: $LOCAL" >> "$LOG_FILE"
        echo "$(date): リモート origin/main: $REMOTE" >> "$LOG_FILE"

        if [ "$LOCAL" != "$REMOTE" ]; then
            echo "$(date): アップデート発見、更新中 (git pull origin main)..." >> "$LOG_FILE"
            git pull origin main >> "$LOG_FILE" 2>&1
            PULL_STATUS=$?
            if [ $PULL_STATUS -ne 0 ]; then
                echo "$(date): git pull origin main 失敗。ステータス: $PULL_STATUS" >> "$LOG_FILE"
            else
                echo "$(date): git pull origin main 成功。" >> "$LOG_FILE"
            fi
            echo "$(date): 更新処理後のGitステータス確認中..." >> "$LOG_FILE"
            git status >> "$LOG_FILE" 2>&1
        else
            echo "$(date): ローカルは最新です。アップデートはありません。" >> "$LOG_FILE"
        fi
    fi
fi
echo "$(date): --- 自動アップデート処理終了 ---" >> "$LOG_FILE"
# --- 自動アップデート処理ここまで ---

echo "$(date): ゲーム起動処理開始..." >> "$LOG_FILE"
python3 main.py 2>&1 | tee -a "$LOG_FILE"
SCRIPT_EXIT_CODE=$?
echo "$(date): main.py スクリプト終了。終了コード: $SCRIPT_EXIT_CODE" >> "$LOG_FILE"
echo "$(date): start_game.sh スクリプト終了" >> "$LOG_FILE"
echo "=====================================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE" # ログの区切りを明確にするための改行

exit $SCRIPT_EXIT_CODE
