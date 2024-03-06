import json
import os


def text_to_danjson(text):
    # text文本转为单轮对话格式
    conversations = []
    paragraphs = text.strip().split('\n\n')

    for paragraph in paragraphs:
        lines = paragraph.strip().split('\n')
        prompt = lines[0]
        response = lines[1]
        conversations.append({'prompt': prompt, 'response': response})

    return json.dumps(conversations, ensure_ascii=False, indent=2)


def text_to_duojson(text):
    # text文本转为 多 轮对话格式
    conversations = []
    paragraphs = text.strip().split('\n\n')

    for paragraph in paragraphs:
        conversation = []
        lines = paragraph.strip().split('\n')
        for i, line in enumerate(lines):
            role = 'system' if i == 0 else 'user' if i % 2 == 1 else 'assistant'
            content = line
            conversation.append({'role': role, 'content': content})
        conversations.append({'conversations': conversation})

    return json.dumps(conversations, ensure_ascii=False, indent=2)


def convert_to_json_file(in_path, out_path, fg):
    # 读取文件内容
    with open(in_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 获取输入文件名（不包含扩展名）
    input_filename = os.path.splitext(os.path.basename(in_path))[0]

    # 将文本转换成JSON格式
    if fg:
        # 多轮
        json_data = text_to_duojson(text)
        fg = '_duo.json'
    else:
        # 单轮
        json_data = text_to_danjson(text)
        fg = '_dan.json'

    # 构建输出文件路径
    output_folder = os.path.join(out_path, 'data_format')
    os.makedirs(output_folder, exist_ok=True)
    output_filename = os.path.join(output_folder, input_filename + fg)

    # 将转换后的JSON数据写入文件
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(json_data)

    print(f"转换完成并已保存为{output_filename}文件。")


# 假设这是你的文本文件路径
input_path = "input_path"
# 指定输出路径
output_path = "output_path"

# 调用函数进行转换并保存为JSON文件
flag = True  # Ture 默认使用多轮对话格式， False 使用单轮对话格式
convert_to_json_file(input_path, output_path, flag)
