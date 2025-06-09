import re
import os


def professional_format_markdown(file_path):
    """
    一个专业的Markdown排版脚本，能实现中文列表的悬挂缩进和内容对齐。
    V3.2 版本：
    - 修正了逻辑错误，并增强了对列表层级回退的处理。
    - 新增功能：将以中文句号或感叹号结尾的行自动添加 <br> 标签。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        # --- 状态机变量 ---
        current_indent_stack = []
        level_indent_stack = []
        in_code_block = False

        # --- 正则表达式 ---
        # 匹配各种列表头
        cn_pattern_1 = re.compile(r'^(\s*)([一二三四五六七八九十]+、)\s*(.*)')
        num_pattern_1 = re.compile(r'^(\s*)(\d+\.)\s*(.*)')
        cn_pattern_2 = re.compile(r'^(\s*)（([一二三四五六七八九十]+)）\s*(.*)')
        num_pattern_2 = re.compile(r'^(\s*)（(\d+)）\s*(.*)')
        bullet_pattern = re.compile(r'^(\s*)([-*+])\s+(.*)')
        patterns = [cn_pattern_1, num_pattern_1, cn_pattern_2, num_pattern_2, bullet_pattern]

        # <<< ADDED: 新增一个正则表达式，用于匹配行尾的 。或 ！>>>
        # r'([。！])$' 解释:
        # [。！] : 匹配列表中的任意一个字符 (。 或 ！)
        # ()     : 将匹配到的字符捕获到分组1中
        # $      : 匹配字符串的末尾
        br_pattern = re.compile(r'([。！])$')

        for line in lines:
            stripped_line = line.rstrip()

            # --- 代码块处理 ---
            if stripped_line.startswith('```'):
                in_code_block = not in_code_block
                current_indent_stack = []
                level_indent_stack = []
                new_lines.append(stripped_line)
                continue

            if in_code_block:
                new_lines.append(line.rstrip('\n'))
                continue

            # 如果是空行，清空状态并添加空行
            if not stripped_line:
                current_indent_stack = []
                level_indent_stack = []
                new_lines.append('')
                continue

            # --- 列表项匹配 ---
            match_found = None
            for pattern in patterns:
                match = pattern.match(line)
                if match:
                    match_found = match
                    break

            # <<< MODIFIED: 统一处理要添加的行，以便应用 <br> 规则 >>>
            line_to_append = ""

            if match_found:
                original_indent_str = match_found.group(1)
                marker = match_found.group(2)
                content = match_found.group(3)
                original_indent_len = len(original_indent_str)

                # 1. 处理层级回退
                while level_indent_stack and original_indent_len < level_indent_stack[-1]:
                    level_indent_stack.pop()
                    current_indent_stack.pop()

                # 2. 处理同级替换
                if level_indent_stack and original_indent_len == level_indent_stack[-1]:
                    level_indent_stack.pop()
                    current_indent_stack.pop()

                # 3. 计算新的悬挂缩进并入栈
                if bullet_pattern.match(line):
                    marker_len = len(marker) + 1
                else:
                    marker_len = len(marker)

                new_hanging_indent = ' ' * (original_indent_len + marker_len + 1)

                level_indent_stack.append(original_indent_len)
                current_indent_stack.append(new_hanging_indent)

                line_to_append = stripped_line

            else:  # 如果不是新的列表项
                if current_indent_stack:
                    indent_str = current_indent_stack[-1]
                    line_to_append = indent_str + stripped_line.lstrip()
                else:
                    line_to_append = stripped_line

            # <<< ADDED: 在将行添加到列表前，应用 <br> 替换规则 >>>
            # br_pattern.sub(r'\1<br>', line_to_append) 解释:
            # \1: 替换为第一个捕获组的内容 (即 。 或 ！)
            # <br>: 在其后追加 <br>
            final_line = br_pattern.sub(r'\1<br>', line_to_append)
            new_lines.append(final_line)

        # 将处理好的行重新组合成文本
        new_content = '\n'.join(new_lines)

        # 写入新文件
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_formatted{ext}"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"专业排版成功！结果已保存至: {output_path}")

    except Exception as e:
        import traceback
        print(f"处理文件时出错 {file_path}: {e}")
        traceback.print_exc()


# --- --- --- --- --- ---
# ---  使 用 指 南  ---
# --- --- --- --- --- ---

if __name__ == "__main__":
    # 请将下面的路径替换成你的Markdown文件路径
    # Windows路径建议使用r''或'/'来避免转义问题
    filename_to_process = r"D:\study\writing\AIchat\Thoughtsfire-inspiringAIchat\社会现象剖析\东亚家庭拧巴.md"

    if os.path.exists(filename_to_process):
        professional_format_markdown(filename_to_process)
    else:
        print(f"错误：文件 '{filename_to_process}' 不存在。")