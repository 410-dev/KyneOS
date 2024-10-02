import System.stdio as stdio
import System.fs as fs
import re

# Usage
#   textutil file.txt instruction
#
# Instructions:
#   - read
#   - write <data>
#   - append <data>
#   - insert <line#> <data>
#   - count <lines/words/chars>
#   - delete <line#>
#   - replace-line <line#> <data>
#   - replace-string <old> <new>
#   - replace-regex <regex> <new>
#   - replace-regex-at <line#> <regex> <new>
#   - find <data>
#   - find-regex <regex>

def unescape_string(s):
    return s.encode('utf-8').decode('unicode_escape')

def main(args: list[str], process):
    args.pop(0)  # Remove the script name from args

    if len(args) < 2:
        stdio.println("Usage: textutil file.txt instruction [parameters]")
        return

    if args[0].startswith("/"):
        filename = args[0]
    else:
        filename = process.cwd + "/" + args[0]
    instruction = args[1]
    lines = []

    if fs.isFile(filename):
        data = fs.reads(filename)
        lines = data.split("\n")
    else:
        stdio.println("File does not exist.")
        return

    if instruction == "read":
        for line in lines:
            stdio.println(line)

    elif instruction == "read-with-line-numbers":
        for idx, line in enumerate(lines, 1):
            stdio.println(f"{idx}: {line}")

    elif instruction == "write":
        if len(args) < 3:
            stdio.println("Usage: write <data>")
            return
        data_to_write = " ".join(args[2:])
        data_to_write = unescape_string(data_to_write)
        fs.writes(filename, data_to_write)

    elif instruction == "append":
        if len(args) < 3:
            stdio.println("Usage: append <data>")
            return
        data_to_append = " ".join(args[2:])
        data_to_append = unescape_string(data_to_append)
        fs.appends(filename, data_to_append)

    elif instruction == "append-line":
        if len(args) < 3:
            stdio.println("Usage: append-line <data>")
            return
        data_to_append = " ".join(args[2:])
        data_to_append = unescape_string(data_to_append)
        lines.append(data_to_append)
        fs.writes(filename, "\n".join(lines))

    elif instruction == "insert":
        if len(args) < 4:
            stdio.println("Usage: insert <line#> <data>")
            return
        try:
            line_num = int(args[2])
            data_to_insert = " ".join(args[3:])
            data_to_insert = unescape_string(data_to_insert)
            lines.insert(line_num - 1, data_to_insert)
            fs.writes(filename, "\n".join(lines))
        except ValueError:
            stdio.println("Line number must be an integer.")

    elif instruction == "count":
        if len(args) < 3:
            stdio.println("Usage: count <lines/words/chars>")
            return
        count_type = args[2]
        if count_type == "lines":
            stdio.println(str(len(lines)))
        elif count_type == "words":
            stdio.println(str(len(data.split())))
        elif count_type == "chars":
            stdio.println(str(len(data)))
        else:
            stdio.println("Unknown count type.")

    elif instruction == "delete":
        if len(args) < 3:
            stdio.println("Usage: delete <line#>")
            return
        try:
            line_num = int(args[2])
            if 1 <= line_num <= len(lines):
                lines.pop(line_num - 1)
                fs.writes(filename, "\n".join(lines))
            else:
                stdio.println("Line number out of range.")
        except ValueError:
            stdio.println("Line number must be an integer.")

    elif instruction == "replace-line":
        if len(args) < 4:
            stdio.println("Usage: replace-line <line#> <data>")
            return
        try:
            line_num = int(args[2])
            new_line = " ".join(args[3:])
            new_line = unescape_string(new_line)
            if 1 <= line_num <= len(lines):
                lines[line_num - 1] = new_line
                fs.writes(filename, "\n".join(lines))
            else:
                stdio.println("Line number out of range.")
        except ValueError:
            stdio.println("Line number must be an integer.")

    elif instruction == "replace-string":
        if len(args) < 4:
            stdio.println("Usage: replace-string <old> <new>")
            return
        old_string = unescape_string(args[2])
        new_string = unescape_string(args[3])
        new_data = data.replace(old_string, new_string)
        fs.writes(filename, new_data)

    elif instruction == "replace-regex":
        if len(args) < 4:
            stdio.println("Usage: replace-regex <regex> <new>")
            return
        regex_pattern = args[2]
        replacement = unescape_string(args[3])
        new_data = re.sub(regex_pattern, replacement, data)
        fs.writes(filename, new_data)

    elif instruction == "replace-regex-at":
        if len(args) < 5:
            stdio.println("Usage: replace-regex-at <line#> <regex> <new>")
            return
        try:
            line_num = int(args[2])
            regex_pattern = args[3]
            replacement = unescape_string(args[4])
            if 1 <= line_num <= len(lines):
                lines[line_num - 1] = re.sub(regex_pattern, replacement, lines[line_num - 1])
                fs.writes(filename, "\n".join(lines))
            else:
                stdio.println("Line number out of range.")
        except ValueError:
            stdio.println("Line number must be an integer.")

    elif instruction == "find":
        if len(args) < 3:
            stdio.println("Usage: find <data>")
            return
        search_str = unescape_string(args[2])
        for idx, line in enumerate(lines, 1):
            if search_str in line:
                stdio.println(f"Line {idx}: {line}")

    elif instruction == "find-line":
        if len(args) < 3:
            stdio.println("Usage: find-line <data>")
            return
        search_str = unescape_string(args[2])
        for idx, line in enumerate(lines, 1):
            if search_str in line:
                stdio.println(f"{line}")

    elif instruction == "find-regex":
        if len(args) < 3:
            stdio.println("Usage: find-regex <regex>")
            return
        regex_pattern = args[2]
        for idx, line in enumerate(lines, 1):
            if re.search(regex_pattern, line):
                stdio.println(f"Line {idx}: {line}")

    else:
        stdio.println("Unknown instruction.")
