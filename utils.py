import io
import json


def create_json(json_path, source, encoding='utf8'):
    with io.open(json_path, 'w', encoding=encoding) as json_file:
        json.dump(source, json_file, ensure_ascii=False, indent=4)
