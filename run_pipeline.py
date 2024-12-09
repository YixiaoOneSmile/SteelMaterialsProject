import subprocess
import argparse
import time
import os
from datetime import datetime
import glob
from typing import List, Set, Tuple

def print_section_header(title):
    """打印带格式的章节标题"""
    print(f"\n{'='*80}")
    print(f"=== {title}")
    print(f"{'='*80}\n")

def print_step(step_num, total_steps, description):
    """打印步骤信息"""
    print(f"\n[步骤 {step_num}/{total_steps}] {description}")
    print("-" * 50)

def run_command(command, description):
    """执行命令并实时输出结果"""
    print(f"\n执行: {' '.join(command)}")
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8'
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
        return_code = process.poll()
        
        if return_code == 0:
            print(f"\n✓ {description}完成")
            return True
        else:
            print(f"\n✗ {description}失败")
            return False
            
    except Exception as e:
        print(f"\n✗ 执行出错: {str(e)}")
        return False

def get_files_to_process(material_name: str, start_time: float = None) -> Tuple[List[str], bool]:
    """
    获取需要处理的文件列表
    返回: (文件列表, 是否为新材料)
    """
    html_path = f"./data/html_data/{material_name}"
    clean_html_path = f"./data/clean_html_data/{material_name}"
    
    # 检查是否为新材料
    is_new_material = not os.path.exists(clean_html_path)
    
    if not os.path.exists(html_path):
        return [], is_new_material
    
    # 获取所有原始HTML文件和已清理的HTML文件
    html_files = set(os.path.splitext(os.path.basename(f))[0] 
                    for f in glob.glob(os.path.join(html_path, "*.html")))
    
    if os.path.exists(clean_html_path):
        clean_files = set(os.path.splitext(os.path.basename(f))[0] 
                         for f in glob.glob(os.path.join(clean_html_path, "*.html")))
    else:
        clean_files = set()
    
    # 找出需要处理的文件
    files_to_process = []
    
    if start_time:
        # 如果指定了开始时间，只处理新爬取的文件
        new_files = [f for f in html_files 
                    if os.path.getctime(os.path.join(html_path, f + ".html")) >= start_time]
        files_to_process.extend(new_files)
    else:
        # 否则处理所有未清理的文件
        files_to_process.extend(html_files - clean_files)
    
    return sorted(files_to_process), is_new_material

def main():
    parser = argparse.ArgumentParser(description='一键执行材料数据处理流程')
    parser.add_argument('-m', '--material', type=str, required=True, help='指定要处理的材料名称')
    parser.add_argument('-s', '--standard', type=str, help='指定材料的对应标准（如包含空格请用引号括起来）', default=None, nargs='+')
    parser.add_argument('--skip-crawl', action='store_true', help='跳过爬取步骤，只执行清理和转换')
    args = parser.parse_args()
    
    start_time = time.time()
    standard = ' '.join(args.standard) if args.standard else None
    
    print_section_header(f"开始处理材料: {args.material}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 如果指定了--skip-crawl，检查材料文件夹是否存在
    if args.skip_crawl:
        if not os.path.exists(f"./data/html_data/{args.material}"):
            print(f"\n错误: 材料 {args.material} 不存在，无法跳过爬取步骤")
            return
        print("\n跳过爬取步骤，直接处理现有文件")
    else:
        # 执行爬取
        print_step(1, 3, "爬取材料数据")
        scraper_command = ['python', 'metal_materials_scraper.py', '-m', args.material]
        if standard:
            scraper_command.extend(['-s', standard])
        
        success = run_command(scraper_command, "数据爬取")
        if not success:
            print("\n爬取数据失败，终止后续步骤")
            return
            
        # 等待文件写入完成
        time.sleep(2)
    
    # 获取需要处理的文件
    if not args.skip_crawl:
        # 如果进行了爬取，只处理新爬取的文件
        files_to_process, _ = get_files_to_process(args.material, start_time)
    else:
        # 否则处理所有未清理的文件
        files_to_process, is_new_material = get_files_to_process(args.material)
    
    if not files_to_process:
        print("\n没有需要处理的新文件")
        return
    
    print(f"\n需要处理的文件数量: {len(files_to_process)}")
    for file in files_to_process:
        print(f"- {file}")
    
    # 步骤2和3: 清理HTML并转换为JSON
    for file in files_to_process:
        # 步骤2: 清理HTML
        print_step(2, 3, f"清理HTML数据 - {file}")
        success = run_command(
            ['python', 'html_cleaner.py', '-m', args.material, '-f', file],
            f"HTML清理 - {file}"
        )
        if not success:
            print(f"\n{file} HTML清理失败，继续处理下一个文件")
            continue
        
        time.sleep(1)
        
        # 步骤3: 转换为JSON
        print_step(3, 3, f"转换为JSON格式 - {file}")
        success = run_command(
            ['python', 'html2Json.py', '-m', args.material, '-f', file],
            f"JSON转换 - {file}"
        )
        if not success:
            print(f"\n{file} JSON转换失败，继续处理下一个文件")
            continue
    
    # 计算总耗时
    end_time = time.time()
    duration = end_time - start_time
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    
    print_section_header("处理完成")
    print(f"材料: {args.material}")
    if args.standard:
        print(f"标准: {' '.join(args.standard)}")
    print(f"处理文件数量: {len(files_to_process)}")
    print(f"总耗时: {minutes}分{seconds}秒")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查并显示生成的文件
    print("\n生成的文件:")
    for file in files_to_process:
        print(f"\n文件组 {file}:")
        
        # 检查原始HTML文件
        html_path = f"./data/html_data/{args.material}/{file}.html"
        if os.path.exists(html_path):
            print(f"- 原始HTML文件: {html_path}")
        
        # 检查清理后的HTML文件
        clean_html_path = f"./data/clean_html_data/{args.material}/{file}.html"
        if os.path.exists(clean_html_path):
            print(f"- 清理后HTML文件: {clean_html_path}")
        
        # 检查JSON文件
        json_path = f"./data/JsonData/{args.material}/{file}.json"
        if os.path.exists(json_path):
            print(f"- JSON文件: {json_path}")

if __name__ == "__main__":
    main() 