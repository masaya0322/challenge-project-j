# database.py Documentation

## 概要

`database.py` は、SQLAlchemy を使用したデータベースモデルの定義ファイルです。
RFID タグの登録情報とスキャン履歴を管理するテーブルを定義します。
タイムゾーンは UTC を使用します。

## テーブル一覧

- **RFIDTag テーブル**:

  - `rfid_tag`: プライマリキー、RFID タグ ID
  - `name`: RFID タグの名前
  - `created_at`: 登録日時（デフォルト: UTC 現在時刻）
  - リレーション: `scanned_records` (ScannedRFID との関連)

- **ScannedRFID テーブル**:
  - `id`: プライマリキー、オートインクリメント
  - `rfid_tag`: 外部キー、RFIDTag.rfid_tag 参照
  - `scanned_at`: スキャン日時（デフォルト: UTC 現在時刻）
  - リレーション: `rfid_tag_relation` (RFIDTag との関連)

## 処理フロー

1. `Base` クラスから継承したモデルクラスを定義。
2. テーブル名とカラムを指定してスキーマを構築。
3. リレーションシップを設定してテーブル間の関連を定義。
