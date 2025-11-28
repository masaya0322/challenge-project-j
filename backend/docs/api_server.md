# API Server Documentation

## 概要

`api_server.py` は、FastAPI フレームワークを使用したバックエンド API サーバーです。
RFID タグの登録情報やスキャン履歴へのアクセスを提供します。
また、データベースの初期化（テーブル作成）もアプリケーション起動時に行います。

### 使用方法

開発サーバーの起動:

```bash
uvicorn backend.api_server:app --reload
```

## 設定項目

- データベース接続設定は `db_connect.py` に依存します。

## 処理フロー

1. **初期化**:

   - `db_connect` からエンジンを取得し、`Base.metadata.create_all` でデータベーステーブルを作成します。

2. **API エンドポイント**:

   - `GET /api/hello`: サーバー稼働確認用。
   - `GET /api/db-check`: データベース接続確認用。
   - `GET /api/rfid-tags`: 登録されている全ての RFID タグ情報を取得します。
   - `GET /api/rfid-tags/{rfid_tag}`: 指定された ID の RFID タグ情報を取得します。
   - `GET /api/currently-scanned-tags`: スキャンされたタグの履歴（`currently_scanned_tags` テーブル）を取得します。

3. **内部ロジック (`handle_rfid_tag_scanned`)**:
   - RFID タグがスキャンされた際に呼び出される関数です（主に `rfid_scanner.py` 等の外部プロセスやロジックから利用されることを想定）。
   - **登録確認**: `rfid_tags` テーブルにタグが存在するか確認し、存在しない場合は新規登録します（デフォルト名: "未登録のおもちゃ"）。
   - **履歴記録**: `currently_scanned_tags` テーブルにスキャン記録を追加します。
