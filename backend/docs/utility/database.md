# database.py Documentation

## 概要

`database.py` は、RFID タグやスキャン履歴のデータベース操作を行うユーティリティ関数群です。
データベースの状態表示、古いスキャン履歴の削除、タグ情報の保存処理などを提供します。

## 設定項目

- データベースのタイムゾーンは UTC で運用されます。
- 削除基準秒数（`delete_old_scanned_records` の `seconds` 引数、デフォルト: 10 秒）

## 処理フロー

1. `print_database_status(db)`：現在の RFID タグ一覧と直近 10 件のスキャン履歴を表示。
2. `delete_old_scanned_records(db, seconds)`：指定秒数より古いスキャン履歴を削除。
3. `process_and_save_tags(inventory_response, db)`：Inventory レスポンスからタグ情報を抽出し、データベースに保存。
   - 新規タグは登録、既存タグは履歴のみ追加。
   - 保存後、データベース状態を表示。
