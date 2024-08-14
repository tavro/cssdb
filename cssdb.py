import re

DATABASE = 'database.css'


def read_data():
    data = {}

    with open(DATABASE, 'r') as file:
        content = file.read()
    
    # find all key-value pairs in the CSS content
    matches = re.findall(r'--([\w-]+):\s*"([^"]+)";', content)
    for key, value in matches:
        data[key] = value
    
    return data


def write_data(data):
    with open(DATABASE, 'w') as file:
        content = ":root {\n"
        for key, value in sorted(data.items()):
            content += f"    --{key}: \"{value}\";\n"
        content += "}\n"
        file.write(content)


def create_record(collection, record):
    data = read_data()
    
    # next unique ID
    record_id = max([int(key.split('-')[1]) for key in data if key.startswith(f"{collection}-")], default=0) + 1
    for record_key, value in record.items():
        css_key = f"{collection}-{record_id}-{record_key}"
        data[css_key] = value
    write_data(data)


def read_records(collection):
    data = read_data()
    records = {}
    for key, value in data.items():
        if key.startswith(f"{collection}-"):
            _, record_id, record_key = key.split('-')
            if record_id not in records:
                records[record_id] = {}
            records[record_id][record_key] = value
    return records


def update_record(collection, record_id, updated_record):
    data = read_data()
    keys_to_remove = [key for key in data.keys() if key.startswith(f"{collection}-{record_id}-")]
    for key in keys_to_remove:
        del data[key]
    for record_key, value in updated_record.items():
        css_key = f"{collection}-{record_id}-{record_key}"
        data[css_key] = value
    write_data(data)


def delete_record(collection, record_id):
    data = read_data()
    keys_to_remove = [key for key in data.keys() if key.startswith(f"{collection}-{record_id}-")]
    for key in keys_to_remove:
        del data[key]
    write_data(data)