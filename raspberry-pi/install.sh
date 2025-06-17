#!/bin/bash
set -e

echo "=== Game IoT ワンライナーセットアップ ==="

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
GAME_DIR="$(dirname "$SCRIPT_DIR")"

echo "ゲームディレクトリ: $GAME_DIR"

# システム更新
#echo "システムを更新中..."
#sudo apt update && sudo apt upgrade -y

# 依存関係インストール
echo "依存関係をインストール中..."
sudo apt install -y git python3-pip python3-pygame python3-venv

# Python仮想環境作成（オプション）
if [ ! -d "$GAME_DIR/venv" ]; then
    echo "Python仮想環境を作成中..."
    python3 -m venv "$GAME_DIR/venv"
fi

# 仮想環境で依存関係インストール
if [ -f "$GAME_DIR/requirements.txt" ]; then
    echo "Python依存関係をインストール中..."
    source "$GAME_DIR/venv/bin/activate"
    pip install -r "$GAME_DIR/requirements.txt"
    deactivate
fi

# 起動スクリプトに実行権限
chmod +x "$SCRIPT_DIR/start_game.sh"

# systemdサービスファイルを動的生成
echo "systemdサービスを設定中..."
sed "s|GAME_DIR_PLACEHOLDER|$GAME_DIR|g" "$SCRIPT_DIR/game-iot.service.template" > /tmp/game-iot.service
sudo mv /tmp/game-iot.service /etc/systemd/system/game-iot.service

# systemd設定
sudo systemctl daemon-reload
sudo systemctl enable game-iot.service

# 自動起動設定（デスクトップ環境用の追加設定）
mkdir -p /home/pi/.config/autostart
cat > /home/pi/.config/autostart/game-iot.desktop << EOF
[Desktop Entry]
Type=Application
Name=Game IoT
Exec=sudo systemctl start game-iot.service
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

echo ""
echo "=== セットアップ完了！ ==="
echo "以下のコマンドで動作確認できます："
echo "  手動起動: sudo systemctl start game-iot.service"
echo "  状態確認: sudo systemctl status game-iot.service"
echo "  ログ確認: journalctl -u game-iot.service -f"
echo ""
echo "再起動後に自動起動します: sudo reboot"