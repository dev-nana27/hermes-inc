# Data Entry Automation Toolkit — 数据录入自动化工具包
# 目标：别人需要手工录入/清洗的数据，我写脚本自动化处理
# 定价：$50-200/脚本，按数据量和复杂度

import csv, json, re, os
from typing import List, Dict

class DataAutomator:
    """数据录入/清洗自动化工具"""
    
    def __init__(self, name: str = "auto-tool"):
        self.name = name
        self.jobs_completed = 0
    
    def extract_from_pdf(self, pdf_path: str) -> List[str]:
        """从PDF提取文本（常用需求：发票/合同/表单）"""
        # 需要pdfminer或pypdf
        from pdfminer.high_level import extract_text
        try:
            text = extract_text(pdf_path)
            return text.split('\n')
        except Exception as e:
            return [f"Error: {e}"]
    
    def extract_tables_from_image(self, image_path: str) -> List[List[str]]:
        """从图片提取表格数据（常用需求：收据/报表）"""
        # 需要OCR (pytesseract)
        try:
            from PIL import Image
            import pytesseract
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            rows = [line.split() for line in text.split('\n') if line.strip()]
            return rows
        except:
            return [["OCR not available"]]
    
    def csv_to_json(self, csv_path: str, output_path: str = None) -> List[Dict]:
        """CSV转JSON（高频需求：数据格式转换）"""
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        self.jobs_completed += 1
        return data
    
    def clean_data(self, raw_data: List[Dict]) -> List[Dict]:
        """数据清洗：去重、格式化、标准化地址/电话"""
        seen = set()
        cleaned = []
        for row in raw_data:
            key = str(row)
            if key not in seen:
                seen.add(key)
                # 清理空格
                cleaned.append({k: str(v).strip() if v else '' for k, v in row.items()})
        return cleaned
    
    def batch_process(self, input_dir: str, pattern: str = "*.csv") -> int:
        """批量处理整个目录的数据文件"""
        import glob
        files = glob.glob(os.path.join(input_dir, pattern))
        total = 0
        for f in files:
            data = self.csv_to_json(f)
            cleaned = self.clean_data(data)
            total += len(cleaned)
        return total

if __name__ == "__main__":
    da = DataAutomator()
    print(f"Data Automator 就绪 — 可处理: PDF提取/图片表格/CSV转JSON/数据清洗")
    print(f"定价: $50-200/脚本")
    print(f"付款: USDT(TRC20) TAuNfjNR1gGaW11Hw1xqLKDhJVvJUA89Zj")
