# バックエンド起動ガイド

## 📝 環境について

このプロジェクトのRFIDスキャナーは**Raspberry Pi**などのLinux環境でのみ動作します。

- ✅ バックエンドAPI、データベース: macOS/Linuxで動作
- ❌ RFIDスキャナー: **Raspberry Piが必要**

**Raspberry Piでのセットアップ方法は `RASPBERRY_PI_SETUP.md` を参照してください。**

## 1. バックエンドとデータベースの起動

### バックエンドディレクトリに移動
```bash
cd backend
```

### Docker Composeで起動
```bash
docker-compose up -d backend db
```

起動するサービス:
- **バックエンドAPI**: http://localhost:8000
- **PostgreSQLデータベース**: localhost:5432

### 起動確認
```bash
# APIの疎通確認
curl http://localhost:8000/api/hello
# => {"message":"Hello World"}

# データベース接続確認
curl http://localhost:8000/api/db-check
# => {"status":"Database connected successfully"}

# ゲーム進行状況を取得
curl http://localhost:8000/api/game/progress
# => {"total_toys":0,"cleaned_toys":0}
```

## 2. フロントエンドと連携して動作確認

### フロントエンドを起動（別ターミナル）
```bash
cd frontend
pnpm dev
```

### 動作確認の流れ
1. ブラウザで http://localhost:3000 を開く
2. タイトル画面からゲームを開始してStageScreenまで進む
3. RFIDリーダーにおもちゃを近づける（自動スキャン）
4. フロントエンドのスコアが自動的に更新されることを確認
5. 全てのタグをスキャンするとリザルト画面に自動遷移することを確認

### スコア計算ルール
- おもちゃ3個ごとにステージアップ
- ステージ1（0-2個目）: 500点/個
- ステージ2（3-5個目）: 1000点/個
- ステージ3（6-8個目）: 1500点/個
- ボーナスステージ（9個目以降）: 2000点/個

例: 6個片付けた場合
```
500×3 + 1000×3 = 4500点
```

## 3. データベースの直接操作

### スキャン履歴をクリア
```bash
docker exec cpj-db psql -U user -d mydb -c "DELETE FROM currently_scanned_tags;"
```

### ゲーム進行状況をリセット
```bash
docker exec cpj-db psql -U user -d mydb -c "UPDATE game_progress SET cleaned_toys = 0;"
```

### 全てのデータをリセット
```bash
docker exec cpj-db psql -U user -d mydb -c "DELETE FROM currently_scanned_tags; DELETE FROM rfid_tags; DELETE FROM game_progress;"
```

## 4. Docker コンテナの操作

### ログを確認
```bash
# バックエンドのログ
docker-compose logs -f backend

# データベースのログ
docker-compose logs -f db
```

### コンテナを停止
```bash
docker-compose down
```

### コンテナを停止してデータも削除
```bash
docker-compose down -v
```

### コンテナを再起動
```bash
docker-compose restart backend
```

## 5. APIエンドポイント一覧

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/api/hello` | GET | API疎通確認 |
| `/api/db-check` | GET | DB接続確認 |
| `/api/rfid-tags` | GET | 登録済みタグ一覧 |
| `/api/rfid-tags/{tag_id}` | GET | 特定のタグ情報 |
| `/api/currently-scanned-tags` | GET | スキャン履歴 |
| `/api/game/progress` | GET | ゲーム進行状況 |

## トラブルシューティング

### ポートが既に使用されている場合
```bash
# 8000番ポートを使用しているプロセスを確認
lsof -i :8000

# 5432番ポートを使用しているプロセスを確認
lsof -i :5432

# プロセスを終了してから再度起動
docker-compose down
docker-compose up -d backend db
```

### データベースの完全リセット
全てのデータ（タグ、スキャン履歴、ゲーム進行状況）を削除して初期状態に戻します。

#### 方法1: スクリプトで全てのタグを削除
```bash
docker exec -it cpj-backend python simulate_rfid.py delete-all
```

#### 方法2: データベースボリュームごと削除（完全リセット）
```bash
docker-compose down -v
docker-compose up -d backend db
```
※ `-v`オプションはボリュームも削除するため、データベースが完全に初期化されます

### Pythonスクリプトでエラーが出る場合
```bash
# Docker コンテナ内で実行
docker exec -it cpj-backend python simulate_rfid.py list
```
