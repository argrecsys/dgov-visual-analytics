# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.4
    Created on: Nov 23, 2023
    Updated on: Dec 12, 2023
    Description: Generate argument data by topics.
"""

import util_libs as ul
import datetime

MAX_TEXT_SIZE = 200


def create_argument_data(proposal_id: int, prop_data: dict, arg_data: dict):
    prop_text = get_comment_text(prop_data["text"])
    prop_short_text = get_comment_short_text(prop_text)

    argument_data = {
        "name": str(proposal_id),
        "children": [],
        "text": prop_text,
        "short_text": prop_short_text,
    }

    arg_cat_ix = 0
    argument_ix = 0
    for arg_cat, arguments in arg_data.items():
        arg_cat_ix += 1
        arg_cat_item = {
            "name": str(arg_cat_ix),
            "children": [],
            "text": arg_cat,
            "short_text": arg_cat,
        }

        for argument in arguments:
            arg_desc = argument["arg_description"]
            arg_intent = "support" if argument["arg_intent"] == "A favor" else "attack"
            arg_text = get_comment_text(f"[{arg_intent.upper()}] {arg_desc}")
            arg_short_text = get_comment_short_text(arg_text)

            argument_ix += 1
            arg_item = {
                "name": str(argument_ix),
                "children": [],
                "text": arg_text,
                "short_text": arg_short_text,
            }

            arg_cat_item["children"].append(arg_item)

        argument_data["children"].append(arg_cat_item)

    return argument_data


def get_comment_text(comment: str, size: int = 10000):
    text = comment.strip()
    text = text.replace("..", ".")
    text = text.replace("  ", " ")
    text = text[:size]
    return text


def get_comment_short_text(comment: str):
    short_comment = comment[:MAX_TEXT_SIZE].strip()
    short_comment = short_comment + ("..." if len(comment) > MAX_TEXT_SIZE else "")
    return short_comment


def load_arguments(input_path: str):
    arguments = {}
    file_path = f"{input_path}/arguments.csv"
    data = ul.read_csv_with_encoding(file_path)

    for index, row in data.iterrows():
        proposal_id = row["proposal_id"]
        comment_id_str = row["comment_id"]
        comment_ids = (
            comment_id_str.replace("[", "").replace("]", "").replace(" ", "").split(",")
        )
        arg_cat = row["arguments name"]
        arg_desc = row["argument_description"]
        arg_intent = row["argument types"]

        categories = arguments.get(proposal_id, {})
        category = categories.get(arg_cat, [])
        category.append(
            {
                "comment_ids": comment_ids,
                "arg_description": arg_desc,
                "arg_intent": arg_intent,
            }
        )
        categories[arg_cat] = category
        arguments[proposal_id] = categories

    return arguments


def main():
    solution_path = "C:/Dev Projects/dgov-visual-analytics"
    input_path = f"{solution_path}/data/raw_data"
    proposals = ul.read_jsonl_data(input_path)
    input_path = f"{solution_path}/data/gpt_data"
    arguments = load_arguments(input_path)
    print(f"Number of proposals: {len(proposals)}")
    print(f"Number of arguments: {len(arguments)}")

    for prop_name, prop_data in proposals.items():
        prop_id = int(prop_name)
        print(f"Proposal: {prop_id}")

        # Filters
        if prop_id not in arguments:
            continue

        arg_data = arguments[prop_id]
        print(f"Argument types: {len(arg_data)}")

        json_data = create_argument_data(prop_id, prop_data[0], arg_data)
        print(f"Number of items: {len(json_data)}")

        output_file = f"{solution_path}/result/json_data/arguments/{prop_name}.json"
        ul.save_dict_to_json(output_file, json_data, 2)


#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    now = datetime.datetime.now()
    print(f">> Run generate argument data ETL- {now}")
    main()
#####################
#### END PROGRAM ####
#####################
