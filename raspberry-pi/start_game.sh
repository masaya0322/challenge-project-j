#!/bin/bash

# 環境変数設定
export DISPLAY=:0
export HOME=/home/aj

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"  
GAME_DIR="$(dirname "$SCRIPT_DIR")"

cd "$GAME_DIR"

# 仮想環境があれば有効化
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 自動アップデート
echo "-----------------------------------------------------" >> logs/game.log
echo "$(date): 自動アップデート処理開始" >> logs/game.log
echo "$(date): 実行ユーザー: $(whoami)" >> logs/game.log
echo "$(date): 現在のディレクトリ: $(pwd)" >> logs/game.log
echo "$(date): Gitステータス確認中..." >> logs/game.log
git status >> logs/game.log 2>&1

echo "$(date): 更新チェック中 (git fetch)..." >> logs/game.log
git fetch origin main >> logs/game.log 2>&1
FETCH_STATUS=$?
if [ $FETCH_STATUS -ne 0 ]; then
    echo "$(date): git fetch 失敗。ステータス: $FETCH_STATUS" >> logs/game.log
else
    echo "$(date): git fetch 成功。" >> logs/game.log
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main)
    echo "$(date): ローカルHEAD: $LOCAL" >> logs/game.log
    echo "$(date): リモート origin/main: $REMOTE" >> logs/game.log

    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "$(date): アップデート発見、更新中 (git pull)..." >> logs/game.log
        git pull origin main >> logs/game.log 2>&1
        PULL_STATUS=$?
        if [ $PULL_STATUS -ne 0 ]; then
            echo "$(date): git pull 失敗。ステータス: $PULL_STATUS" >> logs/game.log
        else
            echo "$(date): git pull 成功。" >> logs/game.log
        fi
        echo "$(date): 更新処理後のGitステータス確認中..." >> logs/game.log
        git status >> logs/game.log 2>&1
    else
        echo "$(date): ローカルは最新です。アップデートはありません。" >> logs/game.log
    fi
fi
echo "$(date): 自動アップデート処理終了" >> logs/game.log
echo "-----------------------------------------------------" >> logs/game.log

# ログディレクトリ作成
mkdir -p logs

# ゲーム起動
echo "$(date): ゲーム起動" >> logs/game.log
python3 main.py 2>&1 | tee -a logs/game.log
