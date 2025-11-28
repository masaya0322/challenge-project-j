from typing import List, Optional
from dataclasses import dataclass

@dataclass
class RfidTag:
    """RFIDタグ情報"""
    pc: str
    epc: str
    rssi: Optional[int] = None
    
    def __str__(self):
        return f"PC: {self.pc}, EPC: {self.epc}"
    
    def __repr__(self):
        return f"RfidTag(pc='{self.pc}', epc='{self.epc}')"
    
    @property
    def full_data(self):
        return self.pc + self.epc

class InventoryResponse:
    """Inventoryレスポンス解析"""
    
    def __init__(self, responses):
        self.raw_responses = responses if isinstance(responses, list) else [responses]
        self.tags: List[RfidTag] = []
        self.total_count: int = 0
        self.success: bool = False
        self._parse_responses()
    
    def _parse_responses(self):
        for response in self.raw_responses:
            hex_data = response.replace(" ", "")
            if len(hex_data) < 16:
                continue
            stx = hex_data[0:2]
            address = hex_data[2:4]
            command = hex_data[4:6]
            data_length = int(hex_data[6:8], 16)
            if stx != "02":
                continue
            if command == "6C":
                self._parse_tag_data(hex_data, data_length)
            elif command == "30":
                self._parse_completion_response(hex_data, data_length)
    
    def _parse_tag_data(self, hex_data: str, data_length: int):
        data_start = 8
        data_end = data_start + (data_length * 2)
        data_part = hex_data[data_start:data_end]
        if len(data_part) < 2:
            return
        rssi_hex = data_part[2:6]
        rssi = int(rssi_hex, 16)
        if len(data_part) < 4:
            return
        pc_epc_length = int(data_part[8:10], 16)
        pc_epc_start = 10
        pc_epc_end = pc_epc_start + (pc_epc_length * 2)
        if len(data_part) < pc_epc_end:
            return
        pc_epc_data = data_part[pc_epc_start:pc_epc_end]
        pc = pc_epc_data[0:4]
        epc = pc_epc_data[4:]
        tag = RfidTag(pc=pc, epc=epc, rssi=rssi)
        self.tags.append(tag)
        pc_formatted = ' '.join(pc[i:i+2] for i in range(0, len(pc), 2))
        epc_formatted = ' '.join(epc[i:i+2] for i in range(0, len(epc), 2))
        print(f"タグ検出 - RSSI: {rssi}, PC: {pc_formatted}, EPC: {epc_formatted}")
    
    def _parse_completion_response(self, hex_data: str, data_length: int):
        data_start = 8
        data_end = data_start + (data_length * 2)
        data_part = hex_data[data_start:data_end]
        if len(data_part) < 8:
            return
        count_low = int(data_part[4:6], 16)
        count_high = int(data_part[6:8], 16)
        self.total_count = (count_high << 8) | count_low
        self.success = True
        print(f"読み取り完了 - 合計 {self.total_count} 枚のタグを検出")
    
    def get_tags(self) -> List[RfidTag]:
        return self.tags
    
    def get_tag_count(self) -> int:
        return len(self.tags)
    
    def is_success(self) -> bool:
        return self.success
    
    def print_tags(self):
        if not self.tags:
            print("\n=== タグ情報 ===")
            print("タグが検出されませんでした。")
            return
        print(f"\n=== タグ情報 ({len(self.tags)}枚検出) ===")
        for i, tag in enumerate(self.tags, 1):
            pc_formatted = ' '.join(tag.pc[j:j+2] for j in range(0, len(tag.pc), 2))
            epc_formatted = ' '.join(tag.epc[j:j+2] for j in range(0, len(tag.epc), 2))
            print(f"\n[タグ #{i}]")
            if tag.rssi is not None:
                print(f"  RSSI: {tag.rssi}")
            print(f"  PC:   {pc_formatted}")
            print(f"  EPC:  {epc_formatted}")
        print(f"\n合計: {self.total_count}枚")
    
    def __str__(self):
        return f"InventoryResponse(success={self.success}, tags={self.get_tag_count()}, total_count={self.total_count})"
    
    def __repr__(self):
        return self.__str__()

def parse_inventory_response(response) -> InventoryResponse:
    """Inventoryレスポンス解析"""
    return InventoryResponse(response)
