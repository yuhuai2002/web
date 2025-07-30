
from flask import Flask, send_file

app = Flask(__name__)

@app.route('/download')
def download_file():
    # 指定文件路径
    file_path = '/root/doc/发票分类.docx'
    # 设置下载后的文件名
    return send_file(file_path, as_attachment=True, download_name="发票分类.docx")

if __name__ == '__main__':
    app.run(debug=True)
