import json 
import os
import importlib


MEMORY_FILE = "memory.json"

write_to_memory_tool = {
    "type": "function",
    "function": {
        "name": "write_to_memory",
        "description": "Write important information to the assistant's memory",
        "parameters": {
            "type": "object",
            "properties": {
            "key": {"type": "string", "description": "The key to store the information under"},
            "value": {"type": "string", "description": "The value to store"}
            },
            "required": ["key", "value"]
        }
    }
}

def write_to_memory(key, value):
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w+') as f:
            json.dump({}, f)

    with open(MEMORY_FILE, 'r+') as f:
        memory = json.load(f)
    memory[key] = value
    with open(MEMORY_FILE, 'w+') as f:
        json.dump(memory, f)
    return f"Stored {value} under {key}."

read_from_memory_tool = {
    "type": "function",
    "function": {
        "name": "read_from_memory",
        "description": "Read important information from the assistant's memory",
        "parameters": {
            "type": "object",
            "properties": {
            "key": {"type": "string", "description": "The key to read the information from"}
            },
            "required": ["key"]
        }
    }
}

def read_from_memory(key):
    with open(MEMORY_FILE, 'r+') as f:
        memory = json.load(f)
    return f"The value stored under {key} is {memory.get(key, 'Key not found')}."

read_file_tool = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read the contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the file"}
            },
            "required": ["file_path"]
        }
    }
}

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"
    
edit_file_tool = {
    "type": "function",
    "function": {
        "name": "edit_file",
        "description": "Edit a file starting in a specific line",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the file"},
                "line_number": {"type": "integer", "description": "Line number to edit from"},
                "new_content": {"type": "string", "description": "New content to write to the file"}
            },
            "required": ["file_path", "line_number", "new_content"]
        }
    }
}

def edit_file(file_path, line_number, new_content):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if line_number > len(lines) or line_number < 1:
            return "Line number out of range."

        lines[line_number - 1] = new_content + "\n"

        with open(file_path, 'w') as file:
            file.writelines(lines)

        return "File edited successfully."
    except Exception as e:
        return f"Error editing file: {e}"

create_file_tool = {
    "type": "function",
    "function": {
        "name": "create_and_write_file",
        "description": "Create a new file and write content to it",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the new file"},
                "content": {"type": "string", "description": "Content to write to the new file"}
            },
            "required": ["file_path", "content"]
        }
    }
}

def create_and_write_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return "File created and content written successfully."
    except Exception as e:
        return f"Error creating or writing to file: {e}"
    
write_new_function_tool = {
    "type": "function",
    "function": {
        "name": "write_new_function",
        "description": "Update the assistant with a new tool",
        "parameters": {
            "type": "object",
            "properties": {
                "new_tool": {"type": "object", "description": "The new tool to add to the assistant in the form of a json. \
                             The json should include 'type' and 'function' keys. \
                             The 'type' key should have the value 'function'. \
                             The 'function' should contain the name of the function, a description, and the parameters. \
                             The parameters should be an object with the keys 'type' 'properties' and 'required'."},
                "function": {"type": "object", "description": "The function to add to the assistant in string form"}
            },
            "required": ["new_tool", "function"]
        }
    }
}

def write_new_function(new_tool: str, function: str, assistant_run):
    tool = json.loads(new_tool)
    name = tool["function"]["name"]
    assistant_run.update(tools=[tool] + assistant_run.tools)
    with open(f"assistant_functions.py", 'a+') as file:
        # write the new tool and the new function to the end of the file
        file.write(f"\n{name}_tool = {json.dumps(tool, indent=4)}\n\n")
        file.write(f"{function}\n\n")
    return f"Tool {name} added successfully."


greet_user_tool = {
    "type": "function",
    "function": {
        "name": "greet_user",
        "description": "Greets the user with the given name.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the person to greet."
                }
            },
            "required": [
                "name"
            ]
        }
    }
}

def greet_user(name: str) -> str:
    return f'Hello, {name}! Welcome to our service. This was edited'


edit_line_tool = {
    "type": "function",
    "function": {
        "name": "edit_line",
        "description": "Edit a specific line in the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file."
                },
                "line_number": {
                    "type": "integer",
                    "description": "The line number to edit."
                },
                "new_content": {
                    "type": "string",
                    "description": "The new content for the specified line."
                }
            },
            "required": [
                "file_path",
                "line_number",
                "new_content"
            ]
        },
        "return": {
            "type": "string",
            "description": "The result of the line editing action."
        }
    }
}

def edit_line(file_path, line_number, new_content):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        if line_number > len(lines) or line_number < 1:
            return "Line number out of range."
        lines[line_number - 1] = new_content + "\n"
        with open(file_path, 'w') as file:
            file.writelines(lines)
        return "File edited successfully."
    except Exception as e:
        return f"Error editing file: {e}"



replace_text_tool = {
    "type": "function",
    "function": {
        "name": "replace_text",
        "description": "Replace all occurrences of a string in the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file."
                },
                "search_string": {
                    "type": "string",
                    "description": "The string to search for in the file."
                },
                "replace_string": {
                    "type": "string",
                    "description": "The string to replace the search string with."
                }
            },
            "required": [
                "file_path",
                "search_string",
                "replace_string"
            ]
        },
        "return": {
            "type": "string",
            "description": "The result of the replace action."
        }
    }
}

def replace_text(file_path, search_string, replace_string):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        new_content = content.replace(search_string, replace_string)
        with open(file_path, 'w') as file:
            file.write(new_content)
        return "Replace action completed successfully."
    except Exception as e:
        return f"Error performing replace action: {e}"



delete_lines_tool = {
    "type": "function",
    "function": {
        "name": "delete_lines",
        "description": "Delete a range of lines in the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file."
                },
                "start_line": {
                    "type": "integer",
                    "description": "The starting line number of the range to delete."
                },
                "end_line": {
                    "type": "integer",
                    "description": "The ending line number of the range to delete."
                }
            },
            "required": [
                "file_path",
                "start_line",
                "end_line"
            ]
        },
        "return": {
            "type": "string",
            "description": "The result of the delete lines action."
        }
    }
}

def delete_lines(file_path, start_line, end_line):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        if start_line < 1 or end_line < start_line:
            return "Invalid range of lines to delete."
        del lines[start_line - 1:end_line]
        with open(file_path, 'w') as file:
            file.writelines(lines)
        return "Delete lines action completed successfully."
    except Exception as e:
        return f"Error performing delete lines action: {e}"



insert_lines_tool = {
    "type": "function",
    "function": {
        "name": "insert_lines",
        "description": "Insert a list of lines into the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file."
                },
                "line_number": {
                    "type": "integer",
                    "description": "The line number at which to insert the new lines."
                },
                "lines": {
                    "type": "array",
                    "description": "The list of new lines to insert.",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
                "file_path",
                "line_number",
                "lines"
            ]
        },
        "return": {
            "type": "string",
            "description": "The result of the insert lines action."
        }
    }
}

def insert_lines(file_path, line_number, lines):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        for i, line in enumerate(lines):
            content.insert(line_number + i - 1, line + '\n')
        with open(file_path, 'w') as file:
            file.writelines(content)
        return "Insert lines action completed successfully."
    except Exception as e:
        return f"Error performing insert lines action: {e}"



get_current_time_and_date_tool = {
    "type": "function",
    "function": {
        "name": "get_current_time_and_date",
        "description": "Get the current time and date.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

from datetime import datetime
def get_current_time_and_date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

