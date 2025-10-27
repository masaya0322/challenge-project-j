import time
import serial
from enum import Enum

# --- 共通設定 ---
FIRST_TIMEOUT = 2.0
READ_TIMEOUT = 0.2

# --- フォーマット関連 ---
def format_hex_with_spaces(hex_string):
    """16進数文字列を2文字ごとに半角スペースで区切る"""
    return ' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))

# --- コマンド送受信 ---
def send_rfid_command(ser, command_hex_string):
    """開いているシリアルポート経由でコマンドを送信し、応答を待つ（複数回受信対応）"""
    try:
        # 送受信バッファをクリア
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # 16進文字列をバイトデータに変換
        command_bytes = bytes.fromhex(command_hex_string)
        
        # コマンド送信
        ser.write(command_bytes)
        formatted_command = format_hex_with_spaces(command_hex_string)
        print(f"送信データ: {formatted_command}")
        
        # 複数回の応答を受信
        response_count = 0
        responses = []

        while True:   
            # 応答を受けた後は、タイムアウトまでの時間を短くする（処理速度を上げるため）
            if response_count == 0:
                ser.timeout = FIRST_TIMEOUT
            else:
                ser.timeout = READ_TIMEOUT

            # 応答受信（終端文字 0x0D まで読み込み、タイムアウトあり）
            response_bytes = ser.read_until(b'\r')  # b'\r' は 0x0D
            
            if response_bytes:
                response_count += 1
                response_bytes_hex_upper = response_bytes.hex().upper()
                formatted_response = format_hex_with_spaces(response_bytes_hex_upper)
                print(f"受信データ #{response_count}: {formatted_response}")
                responses.append(formatted_response)
            else:
                # タイムアウトで応答がなければ終了
                break
        
        # 念の為、コマンド受信後の待機時間を用意
        time.sleep(0.2)

        if response_count == 0:
            print("応答がありませんでした。")
            return None
        elif response_count == 1:
            return responses[0]
        else:
            print(f"合計 {response_count} 件の応答を受信しました。")
            return responses

    except serial.SerialException as e:
        print(f"シリアルポートのエラー: {e}")
        return None

# --- コマンド生成 ---
def generate_full_rfid_command(short_command):
    """短縮コマンドからフルコマンドを生成"""
    hex_list = [short_command[i:i+2] for i in range(0, len(short_command), 2)]
    
    STX_HEX = "02"
    ADDRESS_HEX = "00"
    command_hex = hex_list[0]
    data_length_hex = hex_list[1]
    data_hex_list = hex_list[2:]
    ETX_HEX = "03"

    checksum = 0
    for hex_byte in [STX_HEX, ADDRESS_HEX, command_hex, data_length_hex, *data_hex_list, ETX_HEX]:
        checksum += int(hex_byte, 16)
    checksum_hex = f"{checksum & 0xFF:02X}"

    CR_HEX = "0D"

    full_command = [STX_HEX, ADDRESS_HEX, command_hex, data_length_hex, *data_hex_list, ETX_HEX, checksum_hex, CR_HEX]
    
    command_string = "".join(full_command)
    return command_string

def generate_data_length_part(data_part):
    """データ部からデータ長を計算"""
    byte_length = len(data_part) // 2  # 偶数文字であることが保障されている
    return format(byte_length, '02X')

# --- バリデーション ---
class COMMANDSTATUS(Enum):
    EXIT = 0
    PASS = 1
    REJECT = 2

def is_validation_pass_command(command_name):
    """コマンド名のバリデーション"""
    COMMAND_LENGTH = 2
    if command_name.lower() == "exit":
        return COMMANDSTATUS.EXIT

    if len(command_name) != COMMAND_LENGTH:
        print(f"エラー: コマンド文字数が正しくありません。{COMMAND_LENGTH}文字である必要があります")
        return COMMANDSTATUS.REJECT

    if not all(c in '0123456789ABCDEFabcdef' for c in command_name):
        print("エラー: 16進数のみ入力してください（0-9, A-F）")
        return COMMANDSTATUS.REJECT

    return COMMANDSTATUS.PASS

def is_validation_pass_data(data_part):
    """データ部のバリデーション"""
    if data_part.lower() == "exit":
        return COMMANDSTATUS.EXIT

    if len(data_part) % 2 != 0:
        print("エラー: データ長の文字数が正しくありません")
        return COMMANDSTATUS.REJECT

    if not all(c in '0123456789ABCDEFabcdef' for c in data_part):
        print("エラー: 16進数のみ入力してください（0-9, A-F）")
        return COMMANDSTATUS.REJECT
    
    return COMMANDSTATUS.PASS
