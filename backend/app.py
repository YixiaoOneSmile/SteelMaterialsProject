from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/materials', methods=['GET'])
def get_materials():
    materials_dict = {}  # 使用字典来组织材料数据
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'JsonData')
    
    try:
        if not os.path.exists(base_path):
            return jsonify({"error": f"Directory not found: {base_path}"}), 404
            
        # 遍历所有材料文件夹
        for material_name in os.listdir(base_path):
            material_path = os.path.join(base_path, material_name)
            if os.path.isdir(material_path):
                material_versions = []
                # 获取文件夹中所有的json文件
                json_files = [f for f in os.listdir(material_path) if f.endswith('.json')]
                
                for json_file in json_files:
                    with open(os.path.join(material_path, json_file), 'r', encoding='utf-8') as f:
                        material_data = json.load(f)
                        # 添加标准信息作为版本标识
                        standard_info = material_data.get('Material', {}).get('BelongsToStandard', {})
                        material_versions.append({
                            'data': material_data,
                            'standard': standard_info.get('StandardCode', 'Unknown'),
                            'description': standard_info.get('Description', '')
                        })
                
                # 按 standard 排序
                material_versions.sort(key=lambda x: x['standard'])
                
                if material_versions:
                    materials_dict[material_name] = material_versions
        
        # 将 materials_dict 转换为有序字典并按材料名称排序
        sorted_materials = dict(sorted(materials_dict.items(), key=lambda x: x[0]))
        return jsonify(sorted_materials)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 