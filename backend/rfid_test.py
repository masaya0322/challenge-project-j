# RFID機器に対して任意のコマンドを送ることができる

import sys
import serial
from rfid_connect_util import establish_connection, SERIAL_PORT
from rfid_command_util import (
    send_rfid_command,
    generate_full_rfid_command,
    generate_data_length_part,
    is_validation_pass_command,
    is_validation_pass_data,
    COMMANDSTATUS
)

if __name__ == "__main__":
    # 接続確立
    ser = establish_connection()
    if not ser:
        print("接続の確立に失敗しました。")
        sys.exit(1)

    try:
        # コマンド送信（例：ROMバージョン読み取り）
        print("\n--- ROMバージョン読み取り ---")
        rom_version_command = "02004F019003E50D"
        send_rfid_command(ser, rom_version_command)

        # 任意のコマンドを実行する
        print("\n--- 任意のコマンドを実行する ---")
        print("本来のパケットの中身の順序:[STX][アドレス][コマンド][データ長][データ部][ETX][SUM][CR]")
        print("ここではSTX、ETX、CRなど、毎回固定となる部分を自動的に補完し、簡易的にコマンドを生成できます")
        print("アドレスは00hであることを前提として、SUMやデータ長もマニュアルに基づいて自動計算します")
        print("コマンド名は、第6章や第7章を参照のこと")
        print("データ部は、データを記述してください。空の場合はデータ長は00となります。")
        print("終了する場合はexitと入力してください")

        command_count = 1
        while True:
            print(f"\n <コマンド #{command_count}>")
            print("コマンド名: ", end="")
            command_name = input().strip()
            command_name_status = is_validation_pass_command(command_name)
            
            if command_name_status == COMMANDSTATUS.EXIT:
                break
            elif command_name_status == COMMANDSTATUS.REJECT:
                continue

            print("データ部: ", end="")
            data_part = input().strip()
            data_part_status = is_validation_pass_data(data_part)
            
            if data_part_status == COMMANDSTATUS.EXIT:
                break
            if data_part_status == COMMANDSTATUS.REJECT:
                print("もう一度入力し直してください")
                continue

            data_length_part = generate_data_length_part(data_part)

            short_command = command_name + data_length_part + data_part
            full_command = generate_full_rfid_command(short_command)
            send_rfid_command(ser, full_command)

            command_count += 1

    except serial.SerialException as e:
        print(f"シリアルポートのエラー: {e}")
        sys.exit(1)
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"\n{SERIAL_PORT} を閉じました。")
