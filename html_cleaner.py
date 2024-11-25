from bs4 import BeautifulSoup
import os
import re
from bs4.element import Comment,Tag

def clean_html(html_content):
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 删除位置导航之前的所有内容
    breadcrumb = soup.find('span', class_='layui-breadcrumb')
    if breadcrumb:
        parent_div = breadcrumb.find_parent('div', class_='layui-row')
        if parent_div:
            # 删除该div之前的所有内容
            for element in list(parent_div.previous_siblings):
                if isinstance(element, Tag):
                    element.decompose()
                else:
                    element.extract()
    
    # 删除"注：数据仅供参考"之后的所有内容
    note = soup.find('font', string=lambda x: x and '注：数据仅供参考' in str(x))
    if note:
        parent_div = note.find_parent('div', class_='layui-row')
        if parent_div:
            # 删除该div之后的所有内容
            for element in list(parent_div.next_siblings):
                if isinstance(element, Tag):
                    element.decompose()
                else:
                    element.extract()
            parent_div.decompose()
    
    # 删除所有script标签和onclick等JavaScript事件
    for script in soup.find_all(['script', 'noscript']):
        script.decompose()
    
    # 删除style标签和link标签(CSS)
    for style in soup.find_all(['style', 'link']):
        style.decompose()
    
    # 删除所有注释
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if 'suppliers paihao' in comment:
            # 找到对应的结束注释
            end_comment = comment.find_next(string=lambda text: isinstance(text, Comment) and 'suppliers paihao end' in text)
            if end_comment:
                # 删除这两个注释之间的所有内容
                current = comment
                while current and current != end_comment:
                    next_element = current.next_element
                    current.extract()
                    current = next_element
                end_comment.extract()
        else:
            comment.extract()
    
    # 删除meta标签(保留charset的meta标签)
    for meta in soup.find_all('meta'):
        if not meta.get('charset'):
            meta.decompose()
    
    # 遍历所有标签
    for tag in soup.find_all(True):
        # 删除所有style属性和其他不需要的属性
        attrs = dict(tag.attrs)
        for attr in attrs:
            if attr not in ['charset']:
                del tag[attr]
    
    # 获取处理后的HTML
    cleaned_html = str(soup)
    
    # 删除空行和多余的空白
    cleaned_html = re.sub(r'\n\s*\n', '\n', cleaned_html)
    cleaned_html = re.sub(r'>\s+<', '>\n<', cleaned_html)
    
    return cleaned_html

def process_folder(input_folder, output_folder, material_name=None):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取html_data目录的完整路径
    html_data_dir = os.path.join(input_folder, 'html_data')
    
    # 遍历html_data目录下的所有文件
    for root, dirs, files in os.walk(html_data_dir):
        # 如果指定了材料名称，则只处理对应文件夹
        if material_name:
            current_folder = os.path.basename(root)
            if current_folder != material_name:
                continue
                
        for file in files:
            if file.endswith('.html'):
                # 构建输入文件的完整路径
                input_path = os.path.join(root, file)
                
                # 获取相对路径，保持子文件夹结构
                rel_path = os.path.relpath(root, html_data_dir)
                # 构建输出路径，保持原有的子文件夹结构
                output_dir = os.path.join(output_folder, rel_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_path = os.path.join(output_dir, file)
                
                print(f"处理文件: {input_path}")
                
                try:
                    # 读取HTML文件
                    with open(input_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    # 清理HTML
                    cleaned_html = clean_html(html_content)
                    
                    # 保存清理后的HTML
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_html)
                    
                    print(f"已保存到: {output_path}")
                except Exception as e:
                    print(f"处理文件 {input_path} 时出错: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='清理HTML文件')
    parser.add_argument('--material', type=str, help='指定要处理的材料名称文件夹', default=None)
    args = parser.parse_args()
    
    # 设置输入和输出文件夹
    input_folder = "./data"
    output_folder = "./data/clean_html_data"
    
    # 使用命令行参数调用函数
    process_folder(input_folder, output_folder, args.material)
    
    if args.material:
        print(f"材料 {args.material} 的文件处理完成！")
    else:
        print("所有文件处理完成！") 