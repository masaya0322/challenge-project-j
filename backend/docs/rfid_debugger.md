# RFID Debugger Documentation

## 概要

`rfid_debugger.py` は、RFID リーダーに対して任意のコマンドを送信し、レスポンスを確認するためのデバッグ用スクリプトです。
対話形式でコマンド名とデータ部を入力することで、自動的にパケットを生成して送信します。

## 使用方法

1. スクリプトを実行します。
   ```bash
   python backend/rfid_debugger.py
   ```
2. 接続が成功すると、ROM バージョン読み取りコマンドが送信されます。
3. プロンプトに従ってコマンド名を入力します（例: `55`）。
4. プロンプトに従ってデータ部を入力します（データがない場合は空エンター）。
5. 生成されたコマンドが送信され、レスポンスが表示されます。
6. `exit` と入力すると終了します。

## 処理フロー

1. `utility.rfid_connect.establish_connection` を使用して接続を確立。
2. ROM バージョン読み取りコマンド (`02004F019003E50D`) を送信。
3. ユーザー入力ループ開始:
   - コマンド名入力 (`is_validation_pass_command` で検証)
   - データ部入力 (`is_validation_pass_data` で検証)
   - `generate_data_length_part` でデータ長生成
   - `generate_full_rfid_command` で完全なコマンドパケット生成
   - `send_rfid_command` で送信
