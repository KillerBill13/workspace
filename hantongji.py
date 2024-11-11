import os
import re
from collections import Counter
from pypinyin import pinyin, lazy_pinyin
# 设定文件夹路径
folder_path = '.\language-pack-zh-hans-base_24.10+20241003\language-pack-zh-hans-base\data\zh_CN\LC_MESSAGES'  
# 替换为你的文件夹路径

# 初始化一个 Counter 来累计所有文件的汉字频率
total_char_count = Counter()

# 遍历文件夹中的每个 .po 文件
for filename in os.listdir(folder_path):
    if filename.endswith('.po'):
        file_path = os.path.join(folder_path, filename)
        #print(f"Processing {filename}...")
        
        # 打开文件，读取内容并提取汉字
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
            total_char_count.update(chinese_chars)

# 获取出现次数最多的前十个汉字
top_ten_chars = total_char_count.most_common(10)
print(top_ten_chars)
# 输出前十个汉字及其出现次数
print("\nTop 10 most common Chinese characters:")
for char, count in top_ten_chars:
    print(f"{char}: {count}")
char_pinyin_sorted={}
for char, count in total_char_count.most_common(10):
    pinyinkey=lazy_pinyin(char)[0]

    print(pinyinkey)