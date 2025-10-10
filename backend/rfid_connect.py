import pexpect
import subprocess
import time
import sys
import serial
from enum import Enum

# --- 設定項目 ---
RFID_MAC_ADDRESS = "EC:62:60:C4:A8:36"  # 対象のRFIDリーダーのMACアドレス
SERIAL_PORT = "/dev/rfcomm0"
BAUD_RATE = 115200

def connect_and_pair(mac_address):
    """指定されたMACアドレスのデバイスをスキャンで確認後、接続とペアリングを行う"""
    if not mac_address:
        print("エラー: MACアドレスが指定されていません。")
        return None

    try:
        # bluetoothctlを起動
        child = pexpect.spawn('bluetoothctl', encoding='utf-8')
        print("bluetoothctlを起動しました。")

        # スキャンしてデバイスの存在を確認
        print("デバイスをスキャン中...")
        child.sendline('scan on')
        try:
            # MACアドレスが含まれる行を待つ（タイムアウトは30秒）
            child.expect(f'Device {mac_address}', timeout=30)
            print(f"デバイス {mac_address} を発見しました。")
        except pexpect.exceptions.TIMEOUT:
            print(f"エラー: デバイス {mac_address} が見つかりませんでした。")
            child.sendline('quit')
            return None
        finally:
            # スキャン停止
            child.sendline('scan off')
        
        # ペアリング
        print(f"{mac_address} とペアリングします...")
        child.sendline(f'pair {mac_address}')
        
        # 複数の応答パターンを待つ
        patterns = [
            'Request confirmation',                         # 0: Confirmation needed
            'Failed to pair: org.bluez.Error.AlreadyExists',# 1: Already paired
            'Pairing successful'                            # 2: Pairing successful directly
        ]
        i = child.expect(patterns, timeout=15)
        
        if i == 0: # Confirmation needed
            print("確認リクエストを検出しました。")
            # パスキープロンプトを待つ (正規表現を使用)
            child.expect(r'\[agent\] Confirm passkey \d+ \(yes/no\):', timeout=10)
            print("パスキーの確認プロンプトを検出しました。'yes'を送信します。")
            child.sendline('yes')
            # 'yes'を送信後、ペアリング成功のメッセージを待つ
            child.expect('Pairing successful', timeout=10)
            print("ペアリング成功。")
        elif i == 1: # Already paired
            print("デバイスは既にペアリング済みです。")
        elif i == 2: # Pairing successful
            print("ペアリング成功。")

        # 信頼済みデバイスに設定
        child.sendline(f'trust {mac_address}')
        child.expect('trust succeeded', timeout=10)
        print("信頼済みデバイスに設定しました。")

        # 終了
        child.sendline('quit')
        return mac_address

    except pexpect.exceptions.TIMEOUT:
        print(f"エラー: {mac_address} との接続に失敗しました。")
        return None
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def bind_rfcomm(port, mac_address):
    """MACアドレスを仮想シリアルポートにバインドする"""
    print(f"{mac_address} を {port} にバインドします...")
    try:
        # 既存のバインドを解放（念のため）
        subprocess.run(['sudo', 'rfcomm', 'release', port], check=False)
        time.sleep(1)
        
        # 新しくバインド
        subprocess.run(['sudo', 'rfcomm', 'bind', port, mac_address, '1'], check=True)
        print("バインドに成功しました。")
        time.sleep(2) # デバイスファイルが安定するのを待つ
        return True
    except subprocess.CalledProcessError as e:
        print(f"rfcommのバインドに失敗しました: {e}")
        return False

def send_rfid_command(ser, command_hex_string):
    """開いているシリアルポート経由でコマンドを送信し、応答を待つ"""
    try:
        # 送受信バッファをクリア
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # 16進文字列をバイトデータに変換
        command_bytes = bytes.fromhex(command_hex_string)
        
        # コマンド送信
        ser.write(command_bytes)
        print(f"送信データ: {command_hex_string}")
        
        # デバイスが処理するのを少し待つ
        time.sleep(0.2)
        
        # 応答受信（終端文字 0x0D まで読み込み）
        response_bytes = ser.read_until(b'\r') # b'\r' は 0x0D
        
        if response_bytes:
            print(f"受信データ: {response_bytes.hex().upper()}")
            return response_bytes.hex().upper()
        else:
            print("応答がありませんでした。")
            return None

    except serial.SerialException as e:
        print(f"シリアルポートのエラー: {e}")
        return None

def generate_full_rfid_command(short_command):
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

class COMMANDSTATUS(Enum):
    EXIT = 0
    PASS = 1
    REJECT = 2

def is_validation_pass_command(command_name):
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
    if data_part.lower() == "exit":
        return COMMANDSTATUS.EXIT

    if len(data_part) % 2 != 0:
        print("エラー: データ長の文字数が正しくありません")
        return COMMANDSTATUS.REJECT

    if not all(c in '0123456789ABCDEFabcdef' for c in data_part):
        print("エラー: 16進数のみ入力してください（0-9, A-F）")
        return COMMANDSTATUS.REJECT
    
    return COMMANDSTATUS.PASS

def generate_data_length_part(data_part):
    byte_length = len(data_part) // 2 #偶数文字であることが保障されている
    return format(byte_length, '02X')

if __name__ == "__main__":
    # ステップ1: MACアドレスを指定してペアリング
    target_mac = connect_and_pair(RFID_MAC_ADDRESS)
    if not target_mac:
        sys.exit(1)
        
    # ステップ2: rfcommのバインド
    if not bind_rfcomm(SERIAL_PORT, target_mac):
        sys.exit(1)

    # ステップ3: シリアルポートを開き、コマンドを送信
    ser = None
    try:
        print(f"{SERIAL_PORT} を開いてコマンドを送信します...")
        ser = serial.Serial(
            SERIAL_PORT,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2
        )

        # コマンド送信（例：ROMバージョン読み取り）
        print("\n--- ROMバージョン読み取り ---")
        rom_version_command = "02004F019003E50D"
        send_rfid_command(ser, rom_version_command)

        # コマンド間に十分な待機時間を設ける
        time.sleep(1)

        # 他のコマンドも試せます（例：ブザー制御）
        print("\n--- ブザー制御 ---")
        buzzer_command = "0200420003470D"
        send_rfid_command(ser, buzzer_command)

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

            print("データ部:", end="")
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

    except serial.SerialException as e:
        print(f"シリアルポートのエラー: {e}")
        sys.exit(1)
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"\n{SERIAL_PORT} を閉じました。")
