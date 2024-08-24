import json
import re

def extract_content(messages):
    """Extracts the 'content', 'author', and 'timestamp' values from a list of Discord messages and returns a list of objects."""
    content_list = []
    for message in messages:
        content_list.append({
            'message': message['content'],
            'author': message['author']['username'],
            'timestamp': message['timestamp']
        })
    return content_list

def save_content_to_json(contents, filename):
    """Saves a list of content values to a JSON file."""
    link_free_contents = []
    for content in contents:
        message = re.sub(r'http\S+', '', content['message'])
        link_free_contents.append({
            'message': message,
            'author': content['author'],
            'timestamp': content['timestamp']
        })
    with open(filename, "w") as f:
        json.dump(link_free_contents, f, indent=4)

# Replace 'your_json_file.json' with the actual path to your JSON file
with open("data\\chat_tom.json", encoding="utf-8") as f:
  data = json.load(f)

# Extract the content values
contents = extract_content(data)

# Save the content values to a new JSON file
save_content_to_json(contents, "messages.json")