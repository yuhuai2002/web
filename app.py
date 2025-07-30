import pickle
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import pymysql  # 新增数据库库
import subprocess
import glob
import logging
import time
import zipfile
import json

# --- 修改开始：日志和目录路径 ---
# 将所有路径从宿主机路径改为容器内路径
logging.basicConfig(filename='/app/tmp/flask_upload.log', level=logging.INFO)

# output_dir = "/home/ubuntu/gyd/qianyi/flaskProject-trans/www/output"
output_dir = "/app/www/output" # ✅ 容器内路径

app = Flask(__name__)

# UPLOAD_FOLDER = '/home/ubuntu/gyd/qianyi/flaskProject-trans/www/zip'
UPLOAD_FOLDER = '/app/www/zip' # ✅ 容器内路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# --- 修改结束 ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({'success': False, 'message': '未选择文件'})

    try:
        filename = secure_filename(file.filename) # 使用 secure_filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        logging.info(f"文件已保存到: {save_path}")

        # --- 修改开始：脚本路径 ---
        # script_path = '/home/ubuntu/gyd/qianyi/flaskProject-trans/xgo/Aread_excel.py'
        script_path = '/app/xgo/Aread_excel.py' # ✅ 容器内路径
        # --- 修改结束 ---
        
        python_executable = 'python3'

        # --- 修改开始：日志文件路径 ---
        # with open("/home/ubuntu/gyd/qianyi/flaskProject-trans/tmp/script_output.log", "a") as f:
        with open("/app/tmp/script_output.log", "a") as f: # ✅ 容器内路径
        # --- 修改结束 ---
            process = subprocess.Popen(
                [python_executable, script_path],
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd='/app' # ✅ 设置工作目录，确保 Aread_excel.py 能正确找到相对路径
            )

        return jsonify({
            'success': True,
            'message': f'文件 {filename} 上传成功，并已触发数据处理脚本'
        })
    except Exception as e:
        logging.error(f"上传失败: {str(e)}")
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'})

# ... (delete_all_files 函数保持不变)

@app.route('/data')
def get_data():
    # --- 修改开始：pkl 文件路径 ---
    # file_path = '/home/ubuntu/gyd/qianyi/flaskProject-trans/www/array/list.pkl'
    file_path = '/app/www/array/list.pkl' # ✅ 容器内路径
    # --- 修改结束 ---

    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)

        headers = [
            "Mawb", "Order No", "CTN MARKS", "Reference", "Reference 2",
            "Internal Account Number", "Shipper Name", "Shipper Address 1",
            "Shipper Address 2", "Shipper Address 3", "Shipper City",
            "Shipper State", "Shipper Postcode", "Shipper Country Code",
            "Shipper Turn", "Consignee Name", "Consignee Address1",
            "Consignee Address2", "Consignee Address3", "Consignee City",
            "Consignee State", "Consignee Postcode", "Consignee Country Code",
            "Consignee Email", "Consignee Telephone Number", "Consignee Turn",
            "Consignee VAT Reg No", "Deferment", "GROSS WEIGHT", "Pieces",
            "Weight UOM", "Item Value", "Net Weight", "Currency", "Incoterms",
            "Item Description", "Item HS Code", "Item Quantity", "Total Value",
            "Country Of Origin", "Vendor"
        ]

        return jsonify({
            'success': True,
            'data': data,
            'headers': headers
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/download')
def download_file():
    # --- 修改开始：output 目录路径 ---
    # folder_path = '/home/ubuntu/gyd/qianyi/flaskProject-trans/www/output/'
    folder_path = '/app/www/output/' # ✅ 容器内路径
    # --- 修改结束 ---

    # 获取目录下所有文件，并过滤掉隐藏文件和目录
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        return '目录中没有可下载的文件', 404

    first_file = files[0]  # 取第一个文件
    file_path = os.path.join(folder_path, first_file)
    time.sleep(30)
    return send_file(
        file_path,
        as_attachment=True,
        download_name=first_file,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@app.route('/save-data', methods=['POST'])
def save_data():
    # --- 修改开始：pkl 文件路径 ---
    # file_path = '/home/ubuntu/gyd/qianyi/flaskProject-trans/www/array/list.pkl'
    file_path = '/app/www/array/list.pkl' # ✅ 容器内路径
    # --- 修改结束 ---

    try:
        # 获取前端发送的数据
        received_data = request.get_json()
        new_data = received_data.get('data')

        if not new_data:
            return jsonify({'success': False, 'message': '没有接收到数据'})

        # 写入 pkl 文件
        with open(file_path, 'wb') as f:
            pickle.dump(new_data, f)

        return jsonify({'success': True, 'message': '数据已保存'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)