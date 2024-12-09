import os
from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
from typing import Dict, List
import argparse
import time
import json
# 加载环境变量
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)

def read_html_content(file_path: str) -> str:
    """读取HTML文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def call_openai_api(text: str) -> Dict:
    """调用OpenAI API生成JSON数据"""
    try:
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个金属材料学数据提取专家。请从提供的html网页中中提取以下信息并以JSON格式返回:
                    {
                        "Material": {
                            "Name": "18CrMo4",
                            "OldName": "18CD4",
                            "OtherNames": ["1.7243"],
                            "Category": "合金钢",
                            "Density": "7.85 g/cm³",
                            "BelongsToStandard": {
                            "StandardCode": "NF EN 10084-2008",
                            "Description": "表面硬化结构钢"
                            },
                            "AllStandards": [
                            {
                                "StandardCode": "NF EN 10084-2008",
                                "Description": "表面硬化结构钢"
                            },
                            {
                                "StandardCode": "DIN EN 10084-2008",
                                "Description": "表面硬化钢—技术交货条件"
                            },
                            {
                                "StandardCode": "ISO 683-11-1987",
                                "Description": "热处理钢、合金钢和易切钢 第11部分:表面硬化钢"
                            }
                            ],
                            "Description": "18CrMo4 是一种表面硬化合金结构钢，适用于渗碳处理和高强度要求的零件。"
                        },
                        "ChemicalComposition": {
                            "Elements": {
                            "Fe": { "Min": "-", "Max": "-" },
                            "C": { "Min": "0.15", "Max": "0.21" },
                            "Si": { "Min": "-", "Max": "0.4" },
                            "Mn": { "Min": "0.6", "Max": "0.9" },
                            "Cr": { "Min": "0.9", "Max": "1.2" },
                            "Ni": { "Min": "-", "Max": "-" },
                            "Mo": { "Min": "0.15", "Max": "0.25" },
                            "V": { "Min": "-", "Max": "-" },
                            "Cu": { "Min": "-", "Max": "-" },
                            "N": { "Min": "-", "Max": "-" },
                            "P": { "Min": "-", "Max": "0.025" },
                            "S": { "Min": "-", "Max": "0.035" },
                            "Mg": { "Min": "-", "Max": "-" },
                            "Zn": { "Min": "-", "Max": "-" },
                            "Al": { "Min": "-", "Max": "-" },
                            "W": { "Min": "-", "Max": "-" },
                            "Ti": { "Min": "-", "Max": "-" }
                            },
                            "Notes": [
                            ]
                        },
                        "MechanicalProperties": {
                            "Conditions": [
                            {
                                "Property": "硬度",
                                "Condition": "软化退火（+A）",
                                "Value": "≤207 HBW"
                            },
                            {
                                "Property": "硬度",
                                "Condition": "处理到具有一定硬度（+TH）",
                                "Value": "156~207 HBW"
                            },
                            {
                                "Property": "抗拉强度",
                                "Condition": "室温",
                                "Value": "≥500 MPa"
                            },
                            {
                                "Property": "屈服强度",
                                "Condition": "室温",
                                "Value": "≥205 MPa"
                            }
                            ],
                            "HeatTreatment": [
                            {
                                "Process": "退火",
                                "TemperatureRange": "880°C",
                                "CoolingMethod": "缓冷"
                            },
                            {
                                "Process": "渗碳",
                                "TemperatureRange": "880~980°C",
                                "CoolingMethod": "水冷"
                            },
                            {
                                "Process": "淬火（心部）",
                                "TemperatureRange": "860~900°C",
                                "CoolingMethod": "油冷"
                            },
                            {
                                "Process": "淬火（表层）",
                                "TemperatureRange": "780~820°C",
                                "CoolingMethod": "水冷"
                            },
                            {
                                "Process": "回火",
                                "TemperatureRange": "150~200°C",
                                "CoolingMethod": "空气冷却"
                            }
                            ],
                            "Notes": [
                            ]
                        },
                        "PhysicalProperties": {
                            "Properties": [
                            {
                                "Property": "熔点",
                                "Value": "1420~1460°C"
                            },
                            {
                                "Property": "比热容",
                                "Condition": "20°C",
                                "Value": "0.46 kJ/(kg·K)"
                            },
                            {
                                "Property": "热导率",
                                "Condition": "20°C",
                                "Value": "36 W/(m·K)"
                            },
                            {
                                "Property": "热导率",
                                "Condition": "500°C",
                                "Value": "24 W/(m·K)"
                            },
                            {
                                "Property": "热膨胀系数",
                                "Condition": "20°C",
                                "Value": "11.8 × 10⁻⁶/K"
                            },
                            {
                                "Property": "热膨胀系数",
                                "Condition": "500°C",
                                "Value": "13.2 × 10⁻⁶/K"
                            },
                            {
                                "Property": "电阻率",
                                "Condition": "20°C",
                                "Value": "0.22 Ω·mm²/m"
                            },
                            {
                                "Property": "弹性模量",
                                "Value": "210 GPa"
                            }
                            ]
                        },
                        "SimilarGrades": [
                            {
                            "Field": "保证淬透性结构钢",
                            "Mappings": [
                                {
                                "Standard": "GB",
                                "Grades": ["20CrMnH"]
                                },
                                {
                                "Standard": "NF EN/NF",
                                "Grades": ["18CrMo4"]
                                }
                            ]
                            },
                            {
                            "Field": "合金结构钢",
                            "Mappings": [
                                {
                                "Standard": "JIS",
                                "Grades": ["SCM418"]
                                },
                                {
                                "Standard": "DIN EN/DIN",
                                "Grades": ["18CrMo4", "1.7243"]
                                }
                            ]
                            }
                        ]
                        }
                        注意:
                        1. MechanicalProperties和PhysicalProperties中的数据请根据实际情况生成,如果网页中没有相关数据请仅生成一个空数组。
                        2. 确保返回的JSON数据格式正确，不要包含任何注释以及markdown格式
                        """
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.9,
        )
        return json.loads(clean_json_string(response.choices[0].message.content)) 
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        return None

def clean_json_string(json_string: str) -> str:
    """清理API返回的JSON字符串"""
    # 移除开头的 ```json\n 和结尾的 \n```
    if json_string.startswith('```json\n'):
        json_string = json_string[8:]
    if json_string.endswith('\n```'):
        json_string = json_string[:-4]
    return json_string

def process_folder(base_path: str, output_base_path: str, material_name: str = None, filename: str = None):
    """处理文件夹中的所有HTML文件，每个文件单独生成对应的JSON
    Args:
        base_path: 输入文件夹路径
        output_base_path: 输出文件夹路径
        material_name: 指定要处理的材料名称，默认为None处理所有材料
        filename: 指定要处理的文件名，默认为None处理所有文件
    """
    material_folders = os.listdir(base_path)
    
    # 如果指定了材料名称，只处理该材料
    if material_name:
        if material_name in material_folders:
            material_folders = [material_name]
        else:
            print(f"未找到材料 {material_name} 对应的文件夹")
            return
            
    # 遍历所有子文件夹
    for material_folder in material_folders:
        folder_path = os.path.join(base_path, material_folder)
        if not os.path.isdir(folder_path):
            continue
            
        print(f"\n处理材料文件夹: {material_folder}")
        
        # 创建对应的输出文件夹
        output_folder = os.path.join(output_base_path, material_folder)
        os.makedirs(output_folder, exist_ok=True)

        html_files = os.listdir(folder_path)
        
        # 处理每个HTML文件
        for html_file in html_files:
            if not html_file.endswith('.html'):
                continue
                
            # 如果指定了文件名，则只处理匹配的文件
            if filename and not html_file.startswith(f"{filename}"):
                continue
                
            file_path = os.path.join(folder_path, html_file)
            print(f"处理文件: {html_file}")
            
            try:
                # 读取并处理HTML内容
                text_content = read_html_content(file_path)
                
                # 调用OpenAI API
                json_data = call_openai_api(text_content)
                if json_data:
                    # 生成对应的JSON文件名
                    json_filename = html_file.replace('.html', '.json')
                    json_path = os.path.join(output_folder, json_filename)
                    
                    # 保存单个JSON文件
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"已保存: {json_path}")
                    
                # 添加延迟以避免API限制
                time.sleep(1)
                
            except Exception as e:
                print(f"处理文件 {html_file} 时出错: {str(e)}")
                continue

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将HTML文件转换为JSON格式')
    parser.add_argument('-m', '--material', type=str, help='指定要处理的材料名称', default=None)
    parser.add_argument('-f', '--filename', type=str, help='指定要处理的文件名（如：42CrMo4_20240318_123456）', default=None)
    args = parser.parse_args()
    
    base_path = "./data/clean_html_data"
    output_base_path = "./data/JsonData"
    
    # 创建输出根目录
    os.makedirs(output_base_path, exist_ok=True)
    
    # 处理文件
    process_folder(base_path, output_base_path, args.material, args.filename)
    
    if args.material:
        print(f"\n材料 {args.material} 的转换处理完成!")
        if args.filename:
            print(f"处理的文件: {args.filename}")
    else:
        print("\n所有材料转换处理完成!")

if __name__ == "__main__":
    main()