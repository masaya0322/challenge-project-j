
import time
import serial
from enum import Enum

FIRST_TIMEOUT = 2.0
READ_TIMEOUT = 0.2

def format_hex_with_spaces(hex_string):
    """16進数文字列を2文字ごとに半角スペースで区切る"""
    return ' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))

def send_rfid_command(ser, command_hex_string):
    """シリアルポート経由でコマンド送信・応答受信"""
    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        command_bytes = bytes.fromhex(command_hex_string)
        ser.write(command_bytes)
        formatted_command = format_hex_with_spaces(command_hex_string)
        print(f"送信データ: {formatted_command}")
        response_count = 0
        responses = []
        while True:
            ser.timeout = FIRST_TIMEOUT if response_count == 0 else READ_TIMEOUT
            response_bytes = ser.read_until(b'\r')
            if response_bytes:
                response_count += 1
                response_bytes_hex_upper = response_bytes.hex().upper()
                formatted_response = format_hex_with_spaces(response_bytes_hex_upper)
                print(f"受信データ #{response_count}: {formatted_response}")
                responses.append(formatted_response)
            else:
                break
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

def generate_full_rfid_command(command_name, data_part):
    """
    コマンド名とデータ部からフルコマンドを生成

    入力されたコマンド名とデータ部を基に、通信プロトコルに必要な
    ヘッダー、アドレス、データ長、チェックサム、フッターなどを付与して
    完全なコマンド文字列を生成します。

    Args:
        command_name (str): 2文字の16進数コマンド名（例: "18"）
        data_part (str): 16進数データ文字列（例: "0102"）。空文字も可。

    Returns:
        str: 送信用のフルコマンド文字列。
             構成: STX("02") + アドレス("00") + コマンド + データ長 + データ + ETX("03") + チェックサム + CR("0D")
    """
    STX_HEX = "02"
    ADDRESS_HEX = "00"
    data_length_hex = generate_data_length_part(data_part)
    
    # データ部を2文字ごとのリストに変換
    data_hex_list = [data_part[i:i+2] for i in range(0, len(data_part), 2)]
    
    ETX_HEX = "03"
    checksum = 0
    
    # チェックサム計算対象: STX, ADDRESS, COMMAND, LENGTH, DATA, ETX
    for hex_byte in [STX_HEX, ADDRESS_HEX, command_name, data_length_hex, *data_hex_list, ETX_HEX]:
        checksum += int(hex_byte, 16)
        
    checksum_hex = f"{checksum & 0xFF:02X}"
    CR_HEX = "0D"
    
    full_command = [STX_HEX, ADDRESS_HEX, command_name, data_length_hex, *data_hex_list, ETX_HEX, checksum_hex, CR_HEX]
    command_string = "".join(full_command)
    return command_string

def generate_antenna_setting_command(enable_ant0=True, enable_ant1=False, enable_ant2=False, enable_ant3=False):
    """
    アンテナ有効化設定コマンドを生成

    Args:
        enable_ant0 (bool): アンテナ0の有効化 (Default: True)
        enable_ant1 (bool): アンテナ1の有効化 (Default: False)
        enable_ant2 (bool): アンテナ2の有効化 (Default: False)
        enable_ant3 (bool): アンテナ3の有効化 (Default: False)
    
    Returns:
        str: アンテナ設定変更用のフルコマンド文字列
    """
    antenna_bits = 0
    if enable_ant0:
        antenna_bits |= 1  # bit 0
    if enable_ant1:
        antenna_bits |= 2  # bit 1
    if enable_ant2:
        antenna_bits |= 4  # bit 2
    if enable_ant3:
        antenna_bits |= 8  # bit 3
    
    xx_hex = f"{antenna_bits:02X}"
    # データ部: 33 00 00 80 XX 00 00 00
    data_part = f"33000080{xx_hex}000000"
    
    return generate_full_rfid_command("55", data_part)

def generate_data_length_part(data_part):
    """データ部からデータ長を計算"""
    byte_length = len(data_part) // 2
    return format(byte_length, '02X')

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
