# 钢材数据采集与展示系统    

本项目是一个完整的钢材数据采集和处理系统，包含爬虫、数据清洗、数据转换等功能模块。

## 项目结构

project/
├── metal_materials_scraper.py # 材料数据爬虫
├── html_cleaner.py # HTML数据清洗
├── html2Json.py # HTML转JSON工具
├── frontend/ # 前端展示系统
├── data/ # 数据存储目录
│ ├── html_data/ # 原始HTML数据
│ ├── clean_html_data/ # 清洗后的HTML数据
│ └── JsonData/ # 最终JSON数据
└── requirements.txt # Python依赖文件

## 环境配置
### 1. 创建conda环境
bash
创建新的conda环境
conda create -n material_spider python=3.8
激活环境
conda activate material_spider

### 2. 安装Python依赖
bash
pip install -r requirements.txt

### 3. 安装前端依赖
bash
cd frontend
npm install

### 4. 配置环境变量

1. 复制 `.env.example` 文件并重命名为 `.env`：

bash
cp .env.example .env

2. 编辑 `.env` 文件，填入你的 API 密钥：

bash
openai-cli set-api-key your_api_key_here
openai-cli set-base-url your_base_url_here

## 使用说明

### 1. 材料数据爬虫 (metal_materials_scraper.py)

爬取材料数据的主程序。

**使用方法：**

bash
爬取所有材料数据
python metal_materials_scraper.py
爬取特定材料数据
python metal_materials_scraper.py --material 20Cr

- 不带参数：将爬取预定义列表中的所有材料数据
- `--material`：指定单个材料名称，只爬取该材料的数据

### 2. HTML数据清洗 (html_cleaner.py)

清理原始HTML文件，去除无用标签和内容。

**使用方法：**
bash
清理所有材料的HTML文件
python html_cleaner.py
清理特定材料的HTML文件
python html_cleaner.py --material 20Cr

- 不带参数：清理所有材料文件夹中的HTML文件
- `--material`：只清理指定材料文件夹中的HTML文件

### 3. HTML转JSON工具 (html2Json.py)

将清理后的HTML文件转换为结构化的JSON数据。

**使用方法：**
bash
转换所有材料的HTML文件
python html2Json.py
转换特定材料的HTML文件
python html2Json.py --material 20Cr
- 不带参数：转换所有材料的HTML文件为JSON格式
- `--material`：只转换指定材料的HTML文件为JSON格式

## 数据流向

1. `metal_materials_scraper.py` 爬取原始数据到 `data/html_data/`
2. `html_cleaner.py` 清理数据并保存到 `data/clean_html_data/`
3. `html2Json.py` 转换数据并保存到 `data/JsonData/`

### 4. 前端展示
bash
cd frontend
npm install
npm run dev

### 5. 数据库后端
bash
cd backend
python app.py

## 依赖文件 (requirements.txt)

marker-pdf
selenium
beautifulsoup4
flask
flask-cors
pandas
openai

## License

MIT License