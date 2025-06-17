#!/bin/bash

# 環境変数設定
export DISPLAY=:0
export HOME=/home/pi

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"  
GAME_DIR="$(dirname "$SCRIPT_DIR")"

cd "$GAME_DIR"

# 仮想環境があれば有効化
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 自動アップデート
echo "$(date): 更新チェック中..." >> logs/game.log
git fetch origin main 2>/dev/null || echo "更新チェック失敗"

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date): アップデート発見、更新中..." >> logs/game.log
    git pull origin main
    echo "$(date): 更新完了" >> logs/game.log
fi

# ログディレクトリ作成
mkdir -p logs

# ゲーム起動
echo "$(date): ゲーム起動" >> logs/game.log
python3 main.py 2>&1 | tee -a logs/game.log