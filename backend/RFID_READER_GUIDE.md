# 実際のRFIDリーダーを使用する方法

このガイドでは、実際のUHF RFIDリーダー（Bluetooth接続）を使ってRFIDタグをスキャンし、データベースに登録する方法を説明します。

## ⚠️ 重要な注意事項

**このRFIDスキャナー機能は、Raspberry PiなどのLinux環境でのみ動作します。**

- ✅ **動作する環境**: Raspberry Pi、Ubuntu、Debian などのLinux
- ❌ **動作しない環境**: macOS、Windows

**macOSで開発する場合は、`QUICK_TEST_GUIDE.md`を参照してシミュレーション機能を使用してください。**

## 前提条件

### 必要なハードウェア
- **UHF RFIDリーダー**（Bluetooth対応）
  - MACアドレス: `EC:62:60:C4:A8:36`（デフォルト設定）
  - シリアルポート: `/dev/rfcomm0`
  - ボーレート: 115200

### 必要な環境
- **Linux環境（Raspberry Piなど）** ← 必須
- Bluetooth機能が有効になっている
- Docker & Docker Compose がインストール済み

## 1. RFIDリーダーの接続確認

### 1-1. Bluetoothデバイスのスキャン

```bash
# Dockerコンテナ内でbluetoothctlを起動
docker exec -it cpj-scanner bluetoothctl

# デバイスをスキャン
scan on

# RFIDリーダーのMACアドレスが表示されることを確認
# 例: Device EC:62:60:C4:A8:36 が見つかる

# スキャン停止
scan off
quit
```

### 1-2. 接続テスト（デバッグツール）

RFIDリーダーとの接続をテストします：

```bash
# Dockerコンテナ内でデバッガーを実行
docker exec -it cpj-scanner python rfid_debugger.py
```

成功すると：
- Bluetoothペアリング成功メッセージ
- シリアルポート `/dev/rfcomm0` が開く
- ブザーが鳴る（接続完了）
- ROMバージョン情報が表示される

## 2. RFIDスキャナーの起動

### 2-1. Docker Composeで起動

```bash
cd backend
docker-compose up -d scanner
```

### 2-2. ログを確認

```bash
docker-compose logs -f scanner
```

出力例：
```
scanner  | bluetoothctlを起動しました。
scanner  | デバイスをスキャン中...
scanner  | デバイス EC:62:60:C4:A8:36 を発見しました。
scanner  | ペアリング成功。
scanner  | /dev/rfcomm0 を開きました。
scanner  | 接続完了: ブザーコマンドを送信しました。
scanner  |
scanner  | Inventoryコマンドを1.0秒間隔で実行します。
scanner  | 検出されたタグは自動的にデータベースに保存されます。
scanner  | 10秒以上古いスキャンレコードは自動的に削除されます。
```

## 3. RFIDタグのスキャン

### 3-1. 自動スキャンと登録

RFIDリーダーが起動すると：

1. **1秒ごとに自動スキャン**
   - リーダーの範囲内にあるRFIDタグを検出

2. **自動登録**
   - 新しいタグが検出されると、自動的にデータベースに登録
   - デフォルト名: "未登録のおもちゃ"

3. **スキャン履歴の記録**
   - 検出されたタグは `currently_scanned_tags` テーブルに記録
   - 10秒以上スキャンされていないタグは自動的に削除

### 3-2. スキャン結果の確認

リアルタイムでログを確認：
```bash
docker-compose logs -f scanner
```

出力例：
```
--- 次のタグの処理を開始します: E2801190200050246D8C1B72 ---
新しいRFIDタグを登録しました: E2801190200050246D8C1B72
新しいスキャンレコードとして記録しました: E2801190200050246D8C1B72

===== 現在のRFIDタグ一覧 =====
  RFID: E2801190200050246D8C1B72, 名前: 未登録のおもちゃ, 登録日時: 2024-01-08 15:30:45
```

### 3-3. APIで確認

別ターミナルから：

```bash
# 登録されているタグを確認
curl http://localhost:8000/api/rfid-tags

# スキャン履歴を確認
curl http://localhost:8000/api/currently-scanned-tags

# ゲーム進行状況を確認
curl http://localhost:8000/api/game/progress
```

## 4. RFIDタグに名前を付ける

自動登録されたタグには「未登録のおもちゃ」という名前が付きます。わかりやすい名前に変更しましょう。

### データベースを直接更新

```bash
# タグ一覧を確認
curl http://localhost:8000/api/rfid-tags

# Pythonスクリプトで名前を変更
docker exec cpj-backend python -c "
from db_connect import SessionLocal
from model import RFIDTag

db = SessionLocal()
tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == 'E2801190200050246D8C1B72').first()
if tag:
    tag.name = 'ぬいぐるみ'
    db.commit()
    print(f'タグ名を更新しました: {tag.name}')
db.close()
"
```

または、psqlで直接更新：

```bash
docker exec cpj-db psql -U user -d mydb -c "UPDATE rfid_tags SET name = 'ぬいぐるみ' WHERE rfid_tag = 'E2801190200050246D8C1B72';"
```

## 5. ゲームフローの動作

1. **準備**
   ```bash
   # RFIDスキャナーを起動
   docker-compose up -d scanner

   # バックエンドとDBも起動
   docker-compose up -d backend db
   ```

2. **おもちゃにRFIDタグを貼る**
   - 各おもちゃにRFIDタグを貼り付け
   - 一度スキャンして登録（この時点では「未登録のおもちゃ」）

3. **タグに名前を付ける**
   - 各タグに適切な名前を設定

4. **ゲーム開始**
   - フロントエンドを起動: `cd frontend && pnpm dev`
   - ブラウザで http://localhost:3000 を開く

5. **ゲームプレイ**
   - 子供がおもちゃを片付ける
   - RFIDリーダーの近くに置く
   - 自動的にスキャンされてスコアが加算
   - フロントエンドにリアルタイムで反映

6. **ゲーム終了**
   - 全てのおもちゃを片付けると自動的にリザルト画面に遷移

## 6. トラブルシューティング

### RFIDリーダーが接続できない

```bash
# Bluetoothサービスの状態確認
sudo systemctl status bluetooth

# Bluetoothサービスの再起動
sudo systemctl restart bluetooth

# ペアリング情報をリセット
docker exec -it cpj-scanner bluetoothctl
remove EC:62:60:C4:A8:36
quit

# スキャナーを再起動
docker-compose restart scanner
```

### タグが検出されない

1. **リーダーとタグの距離を確認**
   - UHF RFIDは数cm〜数十cmの範囲で動作
   - タグをリーダーに近づけてみる

2. **アンテナ設定を確認**
   - `rfid_scanner.py` でアンテナ設定を確認
   - デフォルト: Ant0=OFF, Ant1=ON

3. **ログを確認**
   ```bash
   docker-compose logs scanner
   ```

### MACアドレスが異なる場合

`backend/utility/rfid_connect.py` を編集：

```python
RFID_MAC_ADDRESS = "XX:XX:XX:XX:XX:XX"  # 実際のMACアドレス
```

## 7. スキャナーの停止

```bash
# スキャナーのみ停止
docker-compose stop scanner

# 全てのサービスを停止
docker-compose down
```

## 8. 設定ファイル

### RFIDリーダー設定
- **ファイル**: `backend/utility/rfid_connect.py`
- **MACアドレス**: `RFID_MAC_ADDRESS = "EC:62:60:C4:A8:36"`
- **シリアルポート**: `SERIAL_PORT = "/dev/rfcomm0"`
- **ボーレート**: `BAUD_RATE = 115200`

### スキャン間隔
- **ファイル**: `backend/rfid_scanner.py`
- **間隔**: `INVENTORY_INTERVAL = 1.0`（秒）

### 古いレコードの削除時間
- **ファイル**: `backend/rfid_scanner.py`
- **削除条件**: 10秒以上スキャンされていないレコード
- **コード**: `delete_old_scanned_records(db, seconds=10)`

## 9. データベースの直接操作

開発・テスト時にデータベースを直接操作できます：

```bash
# スキャン履歴をクリア
docker exec cpj-db psql -U user -d mydb -c "DELETE FROM currently_scanned_tags;"

# ゲーム進行状況をリセット
docker exec cpj-db psql -U user -d mydb -c "UPDATE game_progress SET cleaned_toys = 0;"

# タグ名を変更
docker exec cpj-db psql -U user -d mydb -c "UPDATE rfid_tags SET name = 'ぬいぐるみ' WHERE rfid_tag = 'E2801190200050246D8C1B72';"

# 全てのデータをリセット
docker exec cpj-db psql -U user -d mydb -c "DELETE FROM currently_scanned_tags; DELETE FROM rfid_tags; DELETE FROM game_progress;"
```
