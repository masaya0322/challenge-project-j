import pexpect
import subprocess
import time
import sys
import serial

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

    except serial.SerialException as e:
        print(f"シリアルポートのエラー: {e}")
        sys.exit(1)
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"\n{SERIAL_PORT} を閉じました。")
