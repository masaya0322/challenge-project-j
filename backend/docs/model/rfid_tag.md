# rfid_tag.py Documentation

## 概要

`rfid_tag.py` は、RFID タグ情報のデータ構造と Inventory コマンドレスポンスの解析を行うクラス群です。
タグの PC、EPC、RSSI 情報を管理し、レスポンスデータを解析してタグリストを生成します。

## タグクラス

- **RfidTag クラス**:

  - `pc`: Protocol Control (2 バイト)
  - `epc`: Electronic Product Code (可変長)
  - `rssi`: 受信信号強度 (オプション)

- **InventoryResponse クラス**:
  - `raw_responses`: 生レスポンスデータ
  - `tags`: 解析された RfidTag リスト
  - `total_count`: 検出タグ総数
  - `success`: 解析成功フラグ

## 処理フロー

1. `InventoryResponse` がレスポンスデータを解析。
2. タグデータレスポンス (コマンド 6C) と完了レスポンス (コマンド 30) を処理。
3. タグデータを PC、EPC、RSSI に分解して `RfidTag` オブジェクトを作成。
4. 完了レスポンスから総タグ数を抽出。
5. `get_tags()`, `is_success()` などで結果を取得。
