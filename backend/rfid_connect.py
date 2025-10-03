import pexpect
import subprocess
import time
import sys
import serial

# --- 設定項目 ---
DEVICE_NAME = "TR3-SPP"  # スキャン時に探すデバイス名
RFID_MAC_ADDRESS = "EC:62:60:C4:A8:37"  # 対象のRFIDリーダーのMACアドレス
SERIAL_PORT = "/dev/rfcomm0"
BAUD_RATE = 115200

def get_mac_and_pair(device_name=None, mac_address=None):
    """bluetoothctlを使ってデバイスをスキャンまたは指定してMACアドレスを取得しペアリングする"""
    try:
        # bluetoothctlを起動
        child = pexpect.spawn('bluetoothctl', encoding='utf-8')
        print("bluetoothctlを起動しました。")

        if mac_address is None:
            if device_name is None:
                print("エラー: device_nameまたはmac_addressを指定してください。")
                return None
            # スキャン開始
            child.sendline('scan on')
            print("デバイスをスキャン中...")

            # デバイス名が含まれる行を待つ（タイムアウトは30秒）
            # 正規表現でMACアドレスを抽出する
            child.expect(r'Device (([0-9A-F]{2}:){5}[0-9A-F]{2}) ' + device_name, timeout=30)
            
            # マッチした部分からMACアドレスを取得
            mac_address = child.match.group(1).decode('utf-8')
            print(f"デバイスを発見しました: {mac_address}")

            # スキャン停止
            child.sendline('scan off')
        else:
            print(f"指定されたMACアドレスを使用します: {mac_address}")
        
        # ペアリング
        print(f"{mac_address} とペアリングします...")
        child.sendline(f'pair {mac_address}')
        i = child.expect(['Pairing successful', 'already paired'], timeout=10)
        if i == 0:
            print("ペアリング成功。")
        else:
            print("デバイスは既にペアリング済みです。")

        # 信頼済みデバイスに設定
        child.sendline(f'trust {mac_address}')
        child.expect('trust succeeded', timeout=10)
        print("信頼済みデバイスに設定しました。")

        # 終了
        child.sendline('quit')
        return mac_address

    except pexpect.exceptions.TIMEOUT:
        if mac_address:
            print(f"エラー: {mac_address} との接続に失敗しました。")
        else:
            print(f"エラー: {device_name} が見つかりませんでした。")
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

def send_rfid_command(port, baudrate, command_hex_string):
    """シリアルポート経由でコマンドを送信し、応答を待つ"""
    ser = None
    try:
        print(f"{port} を開いてコマンドを送信します...")
        ser = serial.Serial(port, baudrate=baudrate, timeout=2) # タイムアウトを2秒に設定
        
        # 16進文字列をバイトデータに変換
        command_bytes = bytes.fromhex(command_hex_string)
        
        # コマンド送信
        ser.write(command_bytes)
        print(f"送信データ: {command_hex_string}")
        
        # 応答受信（最大64バイトまで読み込み）
        response_bytes = ser.read(64)
        
        if response_bytes:
            print(f"受信データ: {response_bytes.hex().upper()}")
            return response_bytes.hex().upper()
        else:
            print("応答がありませんでした。")
            return None

    except serial.SerialException as e:
        print(f"シリアルポートのエラー: {e}")
        return None
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"{port} を閉じました。")


if __name__ == "__main__":
    # ステップ1: MACアドレスを指定してペアリング
    # RFID_MAC_ADDRESSが設定されていればそれを使用し、なければデバイス名でスキャン
    target_mac = get_mac_and_pair(device_name=DEVICE_NAME, mac_address=RFID_MAC_ADDRESS)
    
    if not target_mac:
        sys.exit(1) # MACアドレスが取得できなければ終了
        
    # ステップ2: rfcommのバインド
    if not bind_rfcomm(SERIAL_PORT, target_mac):
        sys.exit(1) # バインドに失敗したら終了

    # ステップ3: コマンドの送信（例：ROMバージョン読み取り）
    # コマンド: 02 00 4F 01 90 03 E5 0D
    rom_version_command = "02004F019003E50D"
    send_rfid_command(SERIAL_PORT, BAUD_RATE, rom_version_command)

    # 他のコマンドも試せます（例：ブザー制御）
    buzzer_command = "0200420003470D"
    send_rfid_command(SERIAL_PORT, BAUD_RATE, buzzer_command)
