import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os
from datetime import datetime
import random

def get_random_user_agent():
    # 基础浏览器和操作系统组件
    browsers = [
        ('Chrome', '119.0.0.0'),
        ('Firefox', '119.0'),
        ('Edge', '119.0.0.0'),
        ('Safari', '17.0'),
        ('Opera', '105.0.0.0')
    ]
    
    os_list = [
        ('Windows NT 10.0; Win64; x64', 'AppleWebKit/537.36 (KHTML, like Gecko)'),
        ('Macintosh; Intel Mac OS X 14_0', 'AppleWebKit/605.1.15 (KHTML, like Gecko)'),
        ('X11; Linux x86_64', 'AppleWebKit/537.36 (KHTML, like Gecko)'),
        ('iPhone; CPU iPhone OS 17_0 like Mac OS X', 'AppleWebKit/605.1.15 (KHTML, like Gecko)'),
        ('Linux; Android 13', 'AppleWebKit/537.36 (KHTML, like Gecko)')
    ]
    
    # 随机选择组件
    browser, version = random.choice(browsers)
    platform, engine = random.choice(os_list)
    
    # 生成随机的次要版本号
    minor_version = f"{random.randint(0,999)}.{random.randint(0,99)}"
    
    # 构建完整的User-Agent
    if 'iPhone' in platform or 'Android' in platform:
        # 移动端格式
        ua = f"Mozilla/5.0 ({platform}) {engine} {browser}/{version}.{minor_version} Mobile Safari/537.36"
    else:
        # 桌面端格式
        ua = f"Mozilla/5.0 ({platform}) {engine} {browser}/{version}.{minor_version} Safari/537.36"
        
    return ua

# 设置options参数
option = ChromeOptions()

# 开启无头模式
# option.add_argument('--headless=new')  # 新版Chrome的无头模式写法

# 开启无痕模式
option.add_argument('--incognito')

# 反爬虫相关设置
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument('--disable-web-security')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('--disable-gpu')
option.add_argument(f'user-agent={get_random_user_agent()}')

# 添加随机窗口大小
widths = [1280, 1366, 1920]
heights = [768, 900, 1080]
option.add_argument(f'--window-size={random.choice(widths)},{random.choice(heights)}')

# 禁用图片加载以提高速度
option.add_argument('--blink-settings=imagesEnabled=false')

# 添加随机延迟函数
def random_sleep():
    time.sleep(random.uniform(2, 5))

def scrape_materials(materials_list, driver, base_url):
    """爬取材料数据的主要函数"""
    try:
        for material_index, material in enumerate(materials_list, 1):
            print(f"\n{'='*50}")
            print(f"正在处理第 {material_index}/{len(materials_list)} 个材料: {material}")
            print(f"{'='*50}")
            
            material_folder = os.path.join('data/html_data', material)
            if not os.path.exists(material_folder):
                os.makedirs(material_folder)

            # 在新标签页打开搜索页面
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(base_url.format(keyword=material))
            random_sleep()

            rows = driver.find_elements(By.XPATH, '//table[@class="layui-table head-sticky"]/tbody/tr')
            print(f"找到 {len(rows)} 个搜索结果")
            
            processed_count = 0
            
            for row_index, row in enumerate(rows, 1):
                try:
                    name_element = WebDriverWait(row, 10).until(
                        EC.visibility_of_element_located((By.XPATH, './td[2]/a'))
                    )
                    name = name_element.text.strip()
                    detail_link = name_element.get_attribute('href')
                except NoSuchElementException:
                    print(f"第 {row_index} 行未找到材料名称元素")
                    continue

                if name.replace(' ', '') == material.replace(' ', ''):
                    processed_count += 1
                    print(f"\n处理进度: {row_index}/{len(rows)} - 当前材料: {name}")
                    
                    # 在新标签页打开详情页
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(detail_link)  # 直接使用get而不是execute_script
                    random_sleep()
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{name}_{timestamp}.html"
                    filepath = os.path.join(material_folder, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    print(f"√ 已保存: {filepath}")

                    # 关闭详情页标签
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                else:
                    print(f"× 跳过第 {row_index} 行 - 材料名称不匹配: {name}")
            
            # 关闭当前材料的搜索页标签
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            print(f"\n{'*'*30}")
            print(f"材料 {material} 处理完成")
            print(f"处理结果: {processed_count}/{len(rows)}")
            print(f"{'*'*30}")

    except Exception as e:
        print(f"\n发生错误: {str(e)}")
    finally:
        print("\n正在关闭浏览器...")
        driver.quit()
        print("任务完成！")

def main():
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='爬取材料数据')
    parser.add_argument('--material', type=str, help='指定要爬取的单个材料', default=None)
    args = parser.parse_args()
    
    # 所有可用的材料列表
    all_materials = ['06Cr19Ni10', '10', '10#', '100C6', '100Cr6', '100Cr6-E', '100Cr6-G', 
                    '100Cr6A', '100CrMnMoSi8-4-6', '100CrMnSi6-4', '100CrMo7-3', '100CrMo7-4', 
                    '10B50', '10MnCrNi', '10MnCrNiMo', '16MnCr5', '16MnCr5H', '18CrMo4', 
                    '18CrNiMo7-6', '18Ni300',  '20Cr', '20CrMnTiH', '20CrMo', '20CrNiMo', 
                    '20MnCr5', '20MnCr5ZR', '31CrMnV9ZR', '34Cr4',  '38CrMoAl', '40Cr', 
                    '42CRMO', '42CrMo4', '440B', '44SMn28', '45#', '50CrMo4', '52100', '55#', 
                    '55#钢', '65Mn', '8620H', '8Cr4Mo4V', '9Cr18Mo', 'C20', 'C45', 'CF53', 
                    'Cr12MoV', 'EP4', 'EP6', 'GCr15', 'GCr15SiMn', 'GCr18Mo', 'K1010',  
                    'M2高速钢', 'M50', 'S43C', 'S45C', 'S53C', 'SAE1055', 'SAE5120', 'SCM415H', 
                    'SCM420H', 'SKF3L', 'SNCM439', 'SUJ2', 'SUJ2S1', 'W6Mo5Cr4V2', 'X45NiCrMo4', 
                    'ZF7B']
    
    # 确定要处理的材料列表
    materials_to_process = [args.material] if args.material else all_materials
    
    if args.material and args.material not in all_materials:
        print(f"警告：材料 '{args.material}' 不在预定义的材料列表中")
        proceed = input("是否继续？(y/n): ")
        if proceed.lower() != 'y':
            print("已取消操作")
            return
    
    # 创建数据目录
    if not os.path.exists('data/html_data'):
        os.makedirs('data/html_data')
    
    # 设置浏览器选项
    option = ChromeOptions()
    # ... 保持原有的浏览器选项设置 ...
    
    print("正在启动浏览器...")
    driver = webdriver.Chrome(option)
    
    # 使用 CDP 命令修改 webdriver 属性
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    base_url = "https://www.caishuku.com/material/?keyword={keyword}"
    
    # 执行爬取
    scrape_materials(materials_to_process, driver, base_url)

if __name__ == "__main__":
    main()