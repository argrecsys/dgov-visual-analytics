# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.1
    Created on: Nov 21, 2023
    Updated on: Nov 23, 2023
    Description: Library of utility functions.
"""

import json
import os
import csv
import pandas as pd


def concatenate_texts_from_jsonl(json_data, field_name):
    concatenated_text = ""
    if json_data:
        texts = [line[field_name] for line in json_data]
        concatenated_text = " ".join(texts)
    return concatenated_text


def load_stopwords(solution_path: str, lang: str):
    stopwords = []

    file_path = f"{solution_path}/nltk_stopwords/{lang}.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        stopwords = [line.rstrip() for line in file]

    return set(stopwords)


def read_csv_with_encoding(filename):
    encodings = ["utf-8", "ISO-8859-1", "latin1", "cp1252"]

    for encoding in encodings:
        try:
            df = pd.read_csv(filename, encoding=encoding)
            print("File successfully read with encoding:", encoding)
            return df
        except UnicodeDecodeError:
            print("Error reading file with encoding:", encoding)

    # Return None if the file could not be read with any encoding
    return None


def read_jsonl_data(folder_path: str):
    # List to store texts
    jsonl_data = {}

    # Get the list of files in the folder
    files = os.listdir(folder_path)
    file_ext = ".jsonl"

    # Process each file in the folder
    for file_name in files:
        # Check if the file is a JSONL file (with extension .jsonl)
        if file_name.endswith(file_ext):
            file_path = os.path.join(folder_path, file_name)
            jsonl = read_jsonl_file(file_path)

            if len(jsonl) > 0:
                jsonl_data[file_name.replace(file_ext, "")] = jsonl

    return jsonl_data


def read_jsonl_file(file_path: str):
    jsonl = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                json_object = json.loads(line)
                jsonl.append(json_object)

    except UnicodeDecodeError as e:
        print(f"Error reading file {file_path}: {e}")

    return jsonl


# Function to remove stopwords
def remove_stopwords(text: str, stopwords, min_size: int = 3):
    words = text.split()
    filtered_words = [
        word for word in words if word.lower() not in stopwords and len(word) > min_size
    ]
    return " ".join(filtered_words)


def save_dict_to_json(output_file: str, data: dict, indent: int):
    if len(data) and indent >= 0:
        # Convert the dictionary to an indented JSON string
        json_data = json.dumps(data, indent=indent)

        # Write the JSON string to a file
        with open(output_file, "w") as file:
            file.write(json_data)


# Using csv.writer method from CSV package
def save_list_to_csv(file_path: str, columns: list, data: list):
    if len(columns) and len(data):
        with open(file_path, "w", newline="") as f:
            write = csv.writer(f)
            write.writerow(columns)
            write.writerows(data)
