import os
import re

# 正则表达式匹配六位数字前缀的文件
pattern = re.compile(r'^\d{6}_')

def rename_files():
    for filename in os.listdir('.'):
        if pattern.match(filename):
            # 提取原数字前缀
            old_prefix = re.match(pattern, filename).group()
            # 计算新前缀，增加四位零
            new_prefix = old_prefix[0:2] + "0000" + old_prefix[2:]
            # 构建新的文件名
            new_filename = new_prefix + filename[len(old_prefix):]
            # 重命名文件
            os.rename(filename, new_filename)
            print(f"{filename} -> {new_filename}")

if __name__ == "__main__":
    rename_files()
    print("重命名完成。")
