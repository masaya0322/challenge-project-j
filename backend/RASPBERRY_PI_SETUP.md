# Raspberry Piセットアップガイド

このガイドでは、Raspberry Pi上でRFIDリーダーを使用する完全なセットアップ手順を説明します。

## 📋 必要なもの

### ハードウェア
- Raspberry Pi（3B+, 4, 5など）
- microSDカード（16GB以上推奨）
- UHF RFIDリーダー（Bluetooth対応）
  - デフォルトMACアドレス: `EC:62:60:C4:A8:36`
- RFIDタグ（UHF対応）

### ソフトウェア
- Raspberry Pi OS（64-bit推奨）
- Docker & Docker Compose

## 🚀 セットアップ手順

### 1. Raspberry Pi OSのインストール

#### Raspberry Pi Imagerを使用（推奨）
1. [Raspberry Pi Imager](https://www.raspberrypi.com/software/)をダウンロード
2. microSDカードを挿入
3. OS選択: **Raspberry Pi OS (64-bit)**
4. 設定（歯車アイコン）:
   - ホスト名: `raspberrypi`
   - SSH有効化: ✅
   - ユーザー名/パスワード設定
   - Wi-Fi設定（必要に応じて）
5. 書き込み開始

### 2. Raspberry Piの初期設定

```bash
# SSHでログイン（macOSから）
ssh pi@raspberrypi.local

# システムアップデート
sudo apt update && sudo apt upgrade -y

# 必要なパッケージをインストール
sudo apt install -y git bluetooth bluez bluez-tools rfkill
```

### 3. Dockerのインストール

```bash
# Dockerインストールスクリプトを実行
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 現在のユーザーをdockerグループに追加
sudo usermod -aG docker $USER

# 再ログイン（グループ変更を反映）
exit
ssh pi@raspberrypi.local

# Dockerバージョン確認
docker --version

# Docker Composeのインストール
sudo apt install -y docker-compose
docker-compose --version
```

### 4. プロジェクトのクローン

```bash
# ホームディレクトリに移動
cd ~

# GitHubからクローン
git clone https://github.com/masaya0322/challenge-project-j.git
cd challenge-project-j/backend
```

### 5. Bluetoothの確認

```bash
# Bluetoothサービスの状態確認
sudo systemctl status bluetooth

# Bluetoothが無効の場合は有効化
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# RFキル（無線機能の無効化）を解除
sudo rfkill unblock bluetooth

# Bluetoothデバイスの確認
bluetoothctl
```

bluetoothctl内で：
```
power on
agent on
default-agent
scan on
```

RFIDリーダーのMACアドレスが表示されることを確認してください。
表示されたら `scan off` で停止し、`quit` で終了。

### 6. RFIDリーダーのMACアドレスを確認・設定

#### MACアドレスを確認
```bash
# スキャンして実際のMACアドレスを確認
bluetoothctl
scan on
# デバイスのMACアドレスをメモ（例: EC:62:60:C4:A8:36）
quit
```

#### デフォルトと異なる場合は設定ファイルを編集
```bash
cd ~/challenge-project-j/backend
nano utility/rfid_connect.py
```

以下の行を実際のMACアドレスに変更：
```python
RFID_MAC_ADDRESS = "XX:XX:XX:XX:XX:XX"  # 実際のMACアドレス
```

### 7. Docker Composeでサービスを起動

```bash
cd ~/challenge-project-j/backend

# 全てのサービスを起動
docker-compose up -d

# ログを確認
docker-compose logs -f
```

成功すると：
```
cpj-backend  | INFO:     Uvicorn running on http://0.0.0.0:8000
cpj-db       | database system is ready to accept connections
cpj-scanner  | bluetoothctlを起動しました。
cpj-scanner  | デバイスをスキャン中...
cpj-scanner  | デバイス EC:62:60:C4:A8:36 を発見しました。
cpj-scanner  | ペアリング成功。
cpj-scanner  | /dev/rfcomm0 を開きました。
cpj-scanner  | 接続完了: ブザーコマンドを送信しました。
```

### 8. 動作確認

#### APIの疎通確認
```bash
# Raspberry Pi上で
curl http://localhost:8000/api/hello
curl http://localhost:8000/api/game/progress
```

#### RFIDタグをスキャン
RFIDタグをリーダーに近づけると、自動的にスキャンされます。

```bash
# スキャナーのログを確認
docker-compose logs -f scanner
```

タグが検出されると：
```
--- 次のタグの処理を開始します: E2801190200050246D8C1B72 ---
新しいRFIDタグを登録しました: E2801190200050246D8C1B72
```

#### 登録されたタグを確認
```bash
docker exec cpj-backend python simulate_rfid.py list
```

#### タグに名前を付ける
```bash
docker exec cpj-backend python simulate_rfid.py rename E2801190200050246D8C1B72 ぬいぐるみ
```

### 9. フロントエンドの起動（オプション）

Raspberry Piでフロントエンドも動かす場合：

```bash
cd ~/challenge-project-j/frontend

# Node.jsのインストール（まだの場合）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# pnpmのインストール
npm install -g pnpm

# 依存関係のインストール
pnpm install

# 開発サーバーを起動
pnpm dev
```

または、別のPC（macOS）からアクセス：
```bash
# macOSのfrontendディレクトリで
# .env.localファイルを作成
echo "NEXT_PUBLIC_API_URL=http://raspberrypi.local:8000" > .env.local

# フロントエンド起動
pnpm dev
```

ブラウザで http://localhost:3000 を開く

## 🎮 ゲームを実行

### 1. おもちゃにRFIDタグを貼る
各おもちゃにRFIDタグを貼り付けます。

### 2. タグを登録
```bash
# タグをリーダーに近づけると自動登録される
# または手動で登録
docker exec cpj-backend python simulate_rfid.py register TAG001 ぬいぐるみ
```

### 3. タグ名を変更
```bash
docker exec cpj-backend python simulate_rfid.py list
docker exec cpj-backend python simulate_rfid.py rename <タグID> <名前>
```

### 4. ゲーム開始
- ブラウザでゲームを開始
- おもちゃを片付ける → リーダーに近づける
- 自動的にスキャン → スコア加算
- 全て片付けるとリザルト画面へ

## 🔧 トラブルシューティング

### RFIDリーダーが見つからない
```bash
# Bluetoothサービス再起動
sudo systemctl restart bluetooth

# スキャン
bluetoothctl
power on
scan on
```

### ペアリングに失敗する
```bash
# 既存のペアリング情報を削除
bluetoothctl
remove EC:62:60:C4:A8:36
quit

# スキャナーコンテナを再起動
docker-compose restart scanner
```

### スキャナーログを確認
```bash
docker-compose logs scanner
```

### データベース接続エラー
```bash
# データベースの状態確認
docker-compose ps

# データベースログ確認
docker-compose logs db

# 再起動
docker-compose restart db backend scanner
```

### タグが検出されない
1. リーダーとタグの距離を調整（数cm〜数十cm）
2. アンテナ設定を確認（rfid_scanner.py）
3. タグが正しいUHF帯域に対応しているか確認

## 📊 コマンド一覧

### サービス管理
```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# 再起動
docker-compose restart

# ログ確認
docker-compose logs -f [service_name]

# 状態確認
docker-compose ps
```

### RFIDタグ管理
```bash
# タグ一覧
docker exec cpj-backend python simulate_rfid.py list

# タグ名変更
docker exec cpj-backend python simulate_rfid.py rename <tag_id> <name>

# タグ削除
docker exec cpj-backend python simulate_rfid.py delete <tag_id>

# 全削除
docker exec -it cpj-backend python simulate_rfid.py delete-all

# スキャン履歴クリア
docker exec cpj-backend python simulate_rfid.py clear

# 進行状況確認
docker exec cpj-backend python simulate_rfid.py progress
```

## 🌐 ネットワーク設定

### 他のデバイスからアクセス

Raspberry PiのIPアドレスを確認：
```bash
hostname -I
```

他のPC（macOSなど）から：
```bash
# バックエンドAPI
curl http://<RaspberryPiのIP>:8000/api/hello

# フロントエンド（Raspberry Piで起動している場合）
http://<RaspberryPiのIP>:3000
```

### ファイアウォール設定（必要に応じて）
```bash
# ポート8000を開放
sudo ufw allow 8000/tcp

# ポート3000を開放（フロントエンド用）
sudo ufw allow 3000/tcp
```

## 🔄 自動起動設定

Raspberry Pi起動時に自動でDockerサービスを起動：

```bash
# Docker起動時に自動起動
cd ~/challenge-project-j/backend
docker-compose up -d

# systemdサービスを作成（オプション）
sudo nano /etc/systemd/system/rfid-game.service
```

rfid-game.service の内容：
```ini
[Unit]
Description=RFID Game Services
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/challenge-project-j/backend
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=pi

[Install]
WantedBy=multi-user.target
```

有効化：
```bash
sudo systemctl enable rfid-game
sudo systemctl start rfid-game
```

## 📝 運用のベストプラクティス

1. **定期的なバックアップ**
   ```bash
   docker-compose exec db pg_dump -U user mydb > backup.sql
   ```

2. **ログのローテーション**
   ```bash
   docker-compose logs --tail=100 > logs.txt
   ```

3. **システムアップデート**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

4. **Dockerイメージの更新**
   ```bash
   cd ~/challenge-project-j/backend
   git pull
   docker-compose build
   docker-compose up -d
   ```

## 🎯 次のステップ

Raspberry Piでの動作確認が完了したら：

1. ✅ バックエンド・DB・スキャナーが正常動作
2. ✅ RFIDタグが自動スキャンされる
3. ✅ フロントエンドでリアルタイム更新
4. ✅ ゲームフローが正常に動作

これで本番環境での運用準備が整いました！
