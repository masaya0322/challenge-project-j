# rfid_connect.py Documentation

## 概要

`rfid_connect.py` は、RFID 機器と Raspberry Pi 間の Bluetooth 接続・シリアル通信の確立を行うユーティリティです。
ペアリング、rfcomm バインド、シリアルポートオープン、接続完了通知（ブザー）などを自動化します。

## 設定項目

- `RFID_MAC_ADDRESS`: 接続対象の RFID リーダー MAC アドレス
- `SERIAL_PORT`: 仮想シリアルポート名（例: `/dev/rfcomm0`）
- `BAUD_RATE`: シリアル通信速度（デフォルト: 115200）

## 処理フロー

1. `connect_and_pair(mac_address)`：Bluetooth デバイスのスキャン・ペアリング・信頼設定。
2. `bind_rfcomm(port, mac_address)`：MAC アドレスを仮想シリアルポートにバインド。
3. `open_serial_port(port, baudrate)`：シリアルポートをオープン。
4. `send_buzzer_command(ser)`：接続完了時にブザーコマンド送信。
5. `establish_connection()`：上記手順をまとめて実行し、シリアルポートオブジェクトを返却。
