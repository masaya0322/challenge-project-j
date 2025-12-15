# RFID Scanner Documentation

## 概要

`rfid_scanner.py` は、RFID リーダーに対して定期的に Inventory コマンドを送信し、検出された RFID タグ情報を取得・データベースへ保存するスクリプトです。

## 設定項目

- `INVENTORY_INTERVAL`: Inventory コマンドの実行間隔（秒）。デフォルトは `1.0` です。

## コマンド詳細

- UHF_Inventory: `02 00 55 01 10 03 6B 0D`
  - タグ情報を取得するために使用されるコマンドです。

## 処理フロー

1. utility の`rfid_connect.py`内の`establish_connction`関数を使って、RFID 機器と通信の確立を行う。失敗した場合は停止。
2. `UHF_Inventory`コマンドを送信する。コマンドを送信する際は、utility の`rfid_command.py`内の`send_rfid_command`関数を使う。
3. レスポンスが成功だったとき、データベースに対して内容を登録する。この際は、utility の`database.py`の`process_and_save_tags`関数を使う。
4. `INVENTORY_INTERVAL`だけ待って、2に戻る
