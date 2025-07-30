import os
import zipfile
import glob

def get_zip_filename(path):
    zip_files = glob.glob(os.path.join(path, '*.zip'))
    if not zip_files:
        raise FileNotFoundError(f"在路径 {path} 下未找到任何 .zip 文件")
    if len(zip_files) > 1:
        raise ValueError(f"路径 {path} 下存在多个 ZIP 文件，请保留一个")
    return zip_files[0]

def unzip_file(zip_path, extract_to=None):
    """
    解压指定路径下的zip压缩包，去除压缩包内的根目录结构
    :param zip_path: zip文件路径
    :param extract_to: 解压目标路径（默认解压到zip文件所在目录）
    :return: 解压后的文件夹路径
    """
    if extract_to is None:
        extract_to = os.path.dirname(zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 获取所有成员路径
        members = zip_ref.namelist()
        
        # 如果所有文件都在同一个根目录下，则去除这个根目录
        common_prefix = os.path.commonprefix(members)
        if common_prefix and all(name.startswith(common_prefix) for name in members):
            # 为每个成员创建新的路径（去除共同前缀）
            for member in members:
                # 跳过目录本身
                if member.endswith('/'):
                    continue
                # 获取去除前缀后的相对路径
                relative_path = member[len(common_prefix):]
                if not relative_path:
                    continue
                # 创建目标路径
                target_path = os.path.join(extract_to, relative_path)
                # 确保目标目录存在
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                # 解压文件
                with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                    target.write(source.read())
        else:
            # 如果没有共同前缀，直接解压所有文件
            zip_ref.extractall(extract_to)
        
    return extract_to

def delete_all_files(path):
    """
    删除指定路径下的所有文件和文件夹
    :param path: 目标路径
    """
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'删除 {file_path} 时出错: {e}')

# 示例用法
if __name__ == "__main__":
    target_path = r'D:\垃圾堆\文档\物流\parcel\zip'  # 替换为你的目标路径
    extracted_path = r'D:\垃圾堆\文档\物流\parcel\unzip'

    # 1. 获取zip文件名
    zip_file = get_zip_filename(target_path)
    if zip_file:
        print(f"找到的zip文件: {zip_file}")
        
        # 2. 解压文件
        extracted_path = unzip_file(zip_file, extracted_path)
        print(f"解压到: {extracted_path}")
        
        # 3. 获取解压后的文件夹路径
        # (已经在unzip_file函数中返回)
        
        # 4. 删除指定路径下的所有文件（谨慎使用！）
        # delete_all_files(target_path)
        # print(f"已删除 {target_path} 下的所有文件")
    else:
        print("未找到zip文件")