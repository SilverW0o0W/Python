#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import csv
import json
from urllib import parse
import requests

SPECIAL_FIELD = "_fields"


class FileType(object):
    UNKNOWN = 0
    JSON = 1
    GZIP = 2
    SUPPORTED_FILE_TYPE = {JSON, GZIP}
    SUPPORTED_CONTENT_TYPE = {"application/x-gzip", "application/json"}
    CONTENT_TYPE_MAP = {
        "application/x-gzip": GZIP,
        "application/json": JSON,
    }


def download_file(url, full_path):
    resp = requests.get(url, stream=True, allow_redirects=True)
    with open(full_path, "wb") as f:
        for content in resp:
            f.write(content)
    return resp.headers.get("Content-Type")


def check_file_type(content_type):
    if content_type not in FileType.SUPPORTED_CONTENT_TYPE:
        return False


def run(url, fields, download_dir_path="."):
    parse_result = parse.urlparse(url)
    full_path = f"{download_dir_path}{os.path.sep}{parse_result.path}"
    if os.path.exists(full_path):
        print("File exists. Skip download.")
        file_type = get_file_type_by_ext(full_path)
    else:
        content_type = download_file(url, full_path)
        file_type = FileType.CONTENT_TYPE_MAP.get(content_type, FileType.UNKNOWN)
    if file_type not in FileType.SUPPORTED_FILE_TYPE:
        print("The file type is not supported yet.")

    fields_dict = load_fields_dict(fields)
    json_file_path = full_path
    if file_type == FileType.JSON:
        results = load_json_file(json_file_path, fields_dict)
        write_csv(json_file_path, results)


def get_file_type_by_ext(full_path):
    ext = os.path.splitext(full_path)[-1]
    if ext == ".json":
        return FileType.JSON
    elif ext == ".gz":
        return FileType.GZIP
    return FileType.UNKNOWN


def write_csv(file_path, rows):
    with open(f"{file_path}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def load_json_file(file_path, fields_dict):
    results = []
    result = load_field_names(fields_dict)
    results.append(result)
    with open(file_path, "r") as f:
        for line in f.readlines():
            result = load_json(line, fields_dict)
            results.append(result)
    return results


def load_json(json_line, fields_dict):
    def _load_json(json_obj, current_level_fields, values):
        json_obj = json.loads(json_obj) if isinstance(json_obj, str) else json_obj
        fields = current_level_fields.get(SPECIAL_FIELD, [])
        for field in fields:
            values.append(json_obj.get(field))
        for field, next_level_fields in current_level_fields.items():
            if field == SPECIAL_FIELD or field not in json_obj:
                continue
            _load_json(json_obj[field], next_level_fields, values)

    result = []
    _load_json(json_line, fields_dict, result)
    return result


def load_field_names(fields_dict):
    def _load_fields_names(path: list, current_level_fields: dict, names: list):
        path_name = ".".join(path)
        for field in current_level_fields.get(SPECIAL_FIELD, []):
            field_name = f"{path_name}.{field}" if path_name else field
            names.append(field_name)

        for field, next_level_fields in current_level_fields.items():
            if field == SPECIAL_FIELD:
                continue
            path.append(field)
            _load_fields_names(path, next_level_fields, names)
            path.pop()

    result = []
    _load_fields_names([], fields_dict, result)
    return result


def load_fields_dict(fields):
    def _load_fields_dict(current_dict, paths):
        if not paths:
            return
        path = paths.pop(0)
        if not paths:
            if SPECIAL_FIELD not in current_dict:
                current_dict[SPECIAL_FIELD] = []
            current_dict[SPECIAL_FIELD].append(path)
        else:
            if path not in current_dict:
                current_dict[path] = {}
            _load_fields_dict(current_dict[path], paths)

    fields_dict = {}
    for field in fields:
        split_paths = field.split(".")
        _load_fields_dict(fields_dict, split_paths)

    return fields_dict


if __name__ == '__main__':
    run("download_url", ["ip", "path", "request.id", ])
