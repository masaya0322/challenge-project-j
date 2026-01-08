# バックエンド起動とRFID動作確認ガイド

## 📝 開発環境について

現在、**macOS**で開発している場合：
- ✅ バックエンドAPI、データベース、フロントエンドは正常に動作します
- ✅ RFIDシミュレーション機能を使ってテストできます
- ❌ 実際のRFIDスキャナーは**Raspberry Pi**などのLinux環境が必要です

**macOSでのテスト方法は `QUICK_TEST_GUIDE.md` を参照してください。**

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

## 2. RFIDタグのシミュレーション

実際のRFIDリーダーがなくても、`simulate_rfid.py`を使ってRFIDスキャンをシミュレートできます。

### 基本的な使い方

スクリプトはDockerコンテナ内で実行します。`docker exec cpj-backend python simulate_rfid.py` の形式で実行してください。

#### 1. RFIDタグを登録
```bash
docker exec cpj-backend python simulate_rfid.py register TAG001 ぬいぐるみ
docker exec cpj-backend python simulate_rfid.py register TAG002 ミニカー
docker exec cpj-backend python simulate_rfid.py register TAG003 ブロック
docker exec cpj-backend python simulate_rfid.py register TAG004 ボール
docker exec cpj-backend python simulate_rfid.py register TAG005 絵本
docker exec cpj-backend python simulate_rfid.py register TAG006 パズル
```

#### 2. 登録されているタグを確認
```bash
docker exec cpj-backend python simulate_rfid.py list
```

出力例:
```
📋 登録されているRFIDタグ:
------------------------------------------------------------
⬜ 未スキャン | TAG001 | ぬいぐるみ
⬜ 未スキャン | TAG002 | ミニカー
⬜ 未スキャン | TAG003 | ブロック
⬜ 未スキャン | TAG004 | ボール
⬜ 未スキャン | TAG005 | 絵本
⬜ 未スキャン | TAG006 | パズル
------------------------------------------------------------

📊 ゲーム進行状況:
   おもちゃ総数: 6
   片付け済み: 0
   進捗率: 0.0%
```

#### 3. RFIDタグをスキャン（おもちゃを片付ける）
```bash
docker exec cpj-backend python simulate_rfid.py scan TAG001
docker exec cpj-backend python simulate_rfid.py scan TAG002
docker exec cpj-backend python simulate_rfid.py scan TAG003
```

出力例:
```
✅ タグをスキャンしました: TAG001 - ぬいぐるみ

📊 ゲーム進行状況:
   おもちゃ総数: 6
   片付け済み: 3
   進捗率: 50.0%
```

#### 4. ゲーム進行状況を確認
```bash
docker exec cpj-backend python simulate_rfid.py progress
```

#### 5. スキャン履歴をクリア（ゲームリセット）
```bash
docker exec cpj-backend python simulate_rfid.py clear
```

#### 6. 特定のRFIDタグを削除
```bash
docker exec cpj-backend python simulate_rfid.py delete TAG001
```

#### 7. 全てのRFIDタグを削除
```bash
# 確認プロンプトが表示されます
docker exec -it cpj-backend python simulate_rfid.py delete-all
```

#### 8. RFIDタグの名前を変更
```bash
# 実機でスキャンしたタグに名前を付ける場合に便利
docker exec cpj-backend python simulate_rfid.py rename E2801190200050246D8C1B72 ぬいぐるみ
```

## 3. フロントエンドと連携して動作確認

### フロントエンドを起動（別ターミナル）
```bash
cd frontend
pnpm dev
```

### 動作確認の流れ
1. ブラウザで http://localhost:3000 を開く
2. タイトル画面からゲームを開始してStageScreenまで進む
3. 別ターミナルで `python simulate_rfid.py scan TAG001` を実行
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
