# rfid_command.py Documentation

## 概要

`rfid_command.py` は、RFID 機器へのコマンド送信・受信、コマンド生成、バリデーションなどを行うユーティリティです。

## 設定項目

- `FIRST_TIMEOUT` (初回応答待ち時間, デフォルト: 2.0 秒)
- `READ_TIMEOUT` (2 回目以降の応答待ち時間, デフォルト: 0.2 秒)

## 処理フロー

1. `send_rfid_command(ser, command_hex_string)`：シリアルポート経由でコマンド送信、応答受信。
2. `generate_full_rfid_command(short_command)`：短縮コマンドからフルコマンド（STX, ETX, SUM, CR 含む）を生成。
3. `generate_data_length_part(data_part)`：データ部からデータ長を計算。
4. `is_validation_pass_command(command_name)`：コマンド名のバリデーション。
5. `is_validation_pass_data(data_part)`：データ部のバリデーション。
