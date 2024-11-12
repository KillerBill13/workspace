import os
import re
from collections import Counter ,defaultdict
from pypinyin import lazy_pinyin
# 设定文件夹路径
folder_path = '.\LC_MESSAGES'  
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
# 输出前十个汉字及其出现次数,以便观察运行情况
print("\nTop 10 most common Chinese characters:")
for char, count in top_ten_chars:
    print(f"{char}: {count}")

# 初始化一个 defaultdict，当访问一个新键时会自动生成空字典
char_pinyin_sorted = defaultdict(dict)

# 按拼音分类汉字
for char, count in total_char_count.most_common():
    pykey = lazy_pinyin(char,strict=False)[0]  # 获取汉字拼音
    # 将汉字和出现次数添加到对应拼音的字典中
    char_pinyin_sorted[pykey][char] = count


# 记录无法自动处理的多音字
manual_adjustment_needed = []

# 打开源字符集文件并逐行处理
with open('pinyin_hanzi.txt', 'r', encoding='utf-8') as infile, \
     open('manual_needed.txt', 'w', encoding='utf-8') as manfile, \
     open('pinyin_hanzi_new.txt', 'w', encoding='utf-8') as outfile:

    # 处理每行的拼音和字符集
    for line in infile:
        # 分割拼音和对应的汉字部分
        parts = line.strip().split()
        if len(parts) < 2:
            print(line.strip(), file=outfile)  # 如果行格式不符合要求则按原样写入
            continue

        pinyin, chars = parts[0], parts[1]

        # 检查拼音是否在统计字典中
        if pinyin not in char_pinyin_sorted:
            # 拼音不在字典中，按原样输出
            print(line.strip(), file=outfile)
            continue

        # 获取该拼音下频率最高的汉字
        most_common_char = max(char_pinyin_sorted[pinyin], key=char_pinyin_sorted[pinyin].get)

        # 判断该汉字是否在字符列表中
        if most_common_char in chars:
            # 如果找到，重新排序使其出现在首位
            chars = most_common_char + chars.replace(most_common_char, "")
        else:
            # 如果未找到，记录为多音字并按原样输出
            manual_adjustment_needed.append(f"{pinyin}: {chars}")
            print(line.strip(), file=outfile)
            continue


        # 将拼音和更新后的字符列表写入输出文件
        print(f"{pinyin} {chars}", file=outfile)

    # 将多音字记录写入文件开头
    print("Manual adjustment needed for the following entries:", file=manfile)
    for entry in manual_adjustment_needed:
        print(entry, file=manfile)
    print("\n", file=manfile)  # 分隔符
    
with open('pinyin_sorted.txt','w',encoding='utf-8') as file:
    for ky in sorted(char_pinyin_sorted):
        print(ky,end=" ",file=file)
        for char in char_pinyin_sorted[ky]:
            print(f'{char}:{char_pinyin_sorted[ky][char]}',end=' ',file=file)
        print(file=file)# 换行
