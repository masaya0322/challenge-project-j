from typing import List, Optional
from dataclasses import dataclass

@dataclass
class RfidTag:
    """RFIDタグの情報を保持するクラス"""
    pc: str  # PC (Protocol Control) - 2バイト
    epc: str  # EPC (Electronic Product Code) - 可変長
    rssi: Optional[int] = None  # 受信信号強度（オプション）
    
    def __str__(self):
        """タグ情報を文字列として表現"""
        return f"PC: {self.pc}, EPC: {self.epc}"
    
    def __repr__(self):
        return f"RfidTag(pc='{self.pc}', epc='{self.epc}')"
    
    @property
    def full_data(self):
        """PCとEPCを結合したフルデータ"""
        return self.pc + self.epc

class InventoryResponse:
    """Inventoryコマンドのレスポンスを解析するクラス"""
    
    def __init__(self, responses):
        """
        Args:
            responses: send_rfid_commandからの返却値（文字列または文字列のリスト）
        """
        self.raw_responses = responses if isinstance(responses, list) else [responses]
        self.tags: List[RfidTag] = []
        self.total_count: int = 0
        self.success: bool = False
        
        self._parse_responses()
    
    def _parse_responses(self):
        """レスポンスを解析してタグ情報を抽出"""
        for response in self.raw_responses:
            # スペースを除去して16進数文字列として扱う
            hex_data = response.replace(" ", "")
            
            # 最低限のデータ長チェック（STX + ADDR + CMD + LEN + ... + ETX + SUM + CR = 最低8バイト）
            if len(hex_data) < 16:
                continue
            
            # データ構造の確認
            stx = hex_data[0:2]
            address = hex_data[2:4]
            command = hex_data[4:6]
            data_length = int(hex_data[6:8], 16)
            
            if stx != "02":  # STXの確認
                continue
            
            # コマンド種別で処理を分岐
            if command == "6C":  # タグデータのレスポンス
                self._parse_tag_data(hex_data, data_length)
            elif command == "30":  # 読み取り完了レスポンス
                self._parse_completion_response(hex_data, data_length)
    
    def _parse_tag_data(self, hex_data: str, data_length: int):
        """タグデータを解析"""
        # データ部の開始位置（STX + ADDR + CMD + LEN = 4バイト = 8文字）
        data_start = 8
        data_end = data_start + (data_length * 2)
        data_part = hex_data[data_start:data_end]
        
        if len(data_part) < 2:
            return
        
        # RSSIを取得（1バイト目）
        rssi_hex = data_part[0:2]
        rssi = int(rssi_hex, 16)
        
        # PC/EPC長を取得（2バイト目）
        if len(data_part) < 4:
            return
        
        pc_epc_length = int(data_part[2:4], 16)
        
        # PC/EPCデータを取得（3バイト目以降）
        pc_epc_start = 4
        pc_epc_end = pc_epc_start + (pc_epc_length * 2)
        
        if len(data_part) < pc_epc_end:
            return
        
        pc_epc_data = data_part[pc_epc_start:pc_epc_end]
        
        # PCは最初の2バイト（4文字）
        pc = pc_epc_data[0:4]
        # EPCはそれ以降
        epc = pc_epc_data[4:]
        
        # RfidTagオブジェクトを作成
        tag = RfidTag(pc=pc, epc=epc, rssi=rssi)
        self.tags.append(tag)
        
        # フォーマットして表示
        pc_formatted = ' '.join(pc[i:i+2] for i in range(0, len(pc), 2))
        epc_formatted = ' '.join(epc[i:i+2] for i in range(0, len(epc), 2))
        print(f"タグ検出 - RSSI: {rssi}, PC: {pc_formatted}, EPC: {epc_formatted}")
    
    def _parse_completion_response(self, hex_data: str, data_length: int):
        """読み取り完了レスポンスを解析"""
        # データ部の開始位置
        data_start = 8
        data_end = data_start + (data_length * 2)
        data_part = hex_data[data_start:data_end]
        
        if len(data_part) < 8:
            return
        
        # 読み取り枚数を取得（3バイト目が下位、4バイト目が上位）
        count_low = int(data_part[4:6], 16)
        count_high = int(data_part[6:8], 16)
        self.total_count = (count_high << 8) | count_low
        
        self.success = True
        print(f"読み取り完了 - 合計 {self.total_count} 枚のタグを検出")
    
    def get_tags(self) -> List[RfidTag]:
        """検出されたタグのリストを返す"""
        return self.tags
    
    def get_tag_count(self) -> int:
        """検出されたタグの数を返す"""
        return len(self.tags)
    
    def is_success(self) -> bool:
        """読み取りが成功したかを返す"""
        return self.success
    
    def print_tags(self):
        """検出されたタグ一覧を整形して表示"""
        if not self.tags:
            print("\n=== タグ情報 ===")
            print("タグが検出されませんでした。")
            return
        
        print(f"\n=== タグ情報 ({len(self.tags)}枚検出) ===")
        for i, tag in enumerate(self.tags, 1):
            # PCをフォーマット
            pc_formatted = ' '.join(tag.pc[j:j+2] for j in range(0, len(tag.pc), 2))
            # EPCをフォーマット
            epc_formatted = ' '.join(tag.epc[j:j+2] for j in range(0, len(tag.epc), 2))
            
            print(f"\n[タグ #{i}]")
            if tag.rssi is not None:
                print(f"  RSSI: {tag.rssi}")
            print(f"  PC:   {pc_formatted}")
            print(f"  EPC:  {epc_formatted}")
        
        print(f"\n合計: {self.total_count}枚")
    
    def __str__(self):
        """レスポンス情報を文字列として表現"""
        return f"InventoryResponse(success={self.success}, tags={self.get_tag_count()}, total_count={self.total_count})"
    
    def __repr__(self):
        return self.__str__()

# ユーティリティ関数
def parse_inventory_response(response) -> InventoryResponse:
    """Inventoryレスポンスを解析してInventoryResponseオブジェクトを返す
    
    Args:
        response: send_rfid_commandからの返却値
        
    Returns:
        InventoryResponse: 解析結果を含むオブジェクト
    """
    return InventoryResponse(response)