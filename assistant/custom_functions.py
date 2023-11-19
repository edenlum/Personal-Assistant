import json

sort_list_tool = {
    "type": "function",
    "function": {
        "name": "sort_list",
        "description": "Sort a list of elements in ascending order.",
        "parameters": {
            "type": "object",
            "properties": {
                "input_list": {"type": "array", "description": "The list of elements to be sorted."}
            },
            "required": ["input_list"]
        }
    }
}

def sort_list(input_list):
    return sorted(input_list) + ["bla"]
    
