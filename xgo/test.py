import glob
import os

extracted_path = "/root/xgo"

for i, file_path in enumerate(sorted(glob.glob(os.path.join(extracted_path, 'Invoice & Packing List/*.xlsx')))):
    print(file_path)