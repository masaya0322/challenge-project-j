
import pexpect
import subprocess
import time
import sys
import serial

RFID_MAC_ADDRESS = "EC:62:60:C4:A8:36"
SERIAL_PORT = "/dev/rfcomm0"
BAUD_RATE = 115200

def connect_and_pair(mac_address):
    """指定されたMACアドレスのデバイスをスキャンで確認後、接続とペアリングを行う"""
    if not mac_address:
        print("エラー: MACアドレスが指定されていません。")
        return None

    try:
        child = pexpect.spawn('bluetoothctl', encoding='utf-8')
        print("bluetoothctlを起動しました。")

        print("デバイスをスキャン中...")
        child.sendline('scan on')
        try:
            child.expect(f'Device {mac_address}', timeout=30)
            print(f"デバイス {mac_address} を発見しました。")
        except pexpect.exceptions.TIMEOUT:
            print(f"エラー: デバイス {mac_address} が見つかりませんでした。")
            child.sendline('quit')
            return None
        finally:
            child.sendline('scan off')
        
        print(f"{mac_address} とペアリングします...")
        child.sendline(f'pair {mac_address}')
        
        patterns = [
            'Request confirmation',                         # 0: Confirmation needed
            'Failed to pair: org.bluez.Error.AlreadyExists',# 1: Already paired
            'Pairing successful'                            # 2: Pairing successful directly
        ]
        i = child.expect(patterns, timeout=15)
        
        if i == 0:
            print("確認リクエストを検出しました。")

            child.expect(r'\[agent\] Confirm passkey \d+ \(yes/no\):', timeout=10)
            print("パスキーの確認プロンプトを検出しました。'yes'を送信します。")
            child.sendline('yes')

            child.expect('Pairing successful', timeout=10)
            print("ペアリング成功。")
        elif i == 1: # Already paired
            print("デバイスは既にペアリング済みです。")
        elif i == 2: # Pairing successful
            print("ペアリング成功。")

        child.sendline(f'trust {mac_address}')
        child.expect('trust succeeded', timeout=10)
        print("信頼済みデバイスに設定しました。")

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
        subprocess.run(['rfcomm', 'release', port], check=False)
        time.sleep(1)

        subprocess.run(['rfcomm', 'bind', port, mac_address, '1'], check=True)
        print("バインドに成功しました。")
        time.sleep(2) # デバイスファイルが安定するのを待つ
        return True
    except subprocess.CalledProcessError as e:
        print(f"rfcommのバインドに失敗しました: {e}")
        return False

def open_serial_port(port, baudrate):
    """シリアルポートを開く"""
    try:
        ser = serial.Serial(
            port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2.0
        )
        print(f"{port} を開きました。")
        return ser
    except serial.SerialException as e:
        print(f"シリアルポートのエラー: {e}")
        return None

def send_buzzer_command(ser):
    """接続完了のブザーコマンドを送信"""
    try:
        buzzer_command = bytes.fromhex("0200420003470D")
        ser.write(buzzer_command)
        print("接続完了: ブザーコマンドを送信しました。")
        time.sleep(0.5)
    except Exception as e:
        print(f"ブザーコマンド送信エラー: {e}")

def establish_connection():
    """RFIDリーダーとの接続を確立し、シリアルポートを返す"""

    target_mac = connect_and_pair(RFID_MAC_ADDRESS)
    if not target_mac:
        return None
        
    if not bind_rfcomm(SERIAL_PORT, target_mac):
        return None

    ser = open_serial_port(SERIAL_PORT, BAUD_RATE)
    if not ser:
        return None

    send_buzzer_command(ser)
    
    return ser

if __name__ == "__main__":
    ser = establish_connection()
    if ser:
        print("\n接続が確立されました。")
        ser.close()
        print(f"{SERIAL_PORT} を閉じました。")
    else:
        print("接続の確立に失敗しました。")
        sys.exit(1)
