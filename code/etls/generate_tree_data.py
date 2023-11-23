# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.1
    Created on: Nov 23, 2023
    Updated on: Nov 23, 2023
    Description: Main class.
"""
import util_libs as ul
import pandas as pd


def create_proposal_data(
    proposal_name: str, proposal_hierarchy: dict, comments_text: dict
):
    prop_text = get_comment_text(comments_text, int(proposal_name))
    proposal_data = {
        "name": prop_text[:50],
        "children": [],
        "text": prop_text,
    }
    parent_id = -1
    print(len(proposal_hierarchy))

    proposal_data["children"] = __create_proposal_data_inner(
        proposal_data["children"], proposal_hierarchy, comments_text, parent_id
    )

    return proposal_data


def __create_proposal_data_inner(
    proposal_data: list,
    proposal_hierarchy: dict,
    comments_text: dict,
    parent_id: int = -1,
):
    comment_ids = proposal_hierarchy["comment_ids"]
    parent_ids = proposal_hierarchy["parent_ids"]

    for curr_comment_id, curr_parent_id in zip(comment_ids, parent_ids):
        if curr_parent_id == parent_id:
            prop_text = get_comment_text(comments_text, curr_comment_id)
            if curr_comment_id in parent_ids:
                item = {
                    "name": prop_text[:50],
                    "children": [],
                    "text": prop_text,
                }
                proposal_data.append(item)
                __create_proposal_data_inner(
                    item["children"], proposal_hierarchy, comments_text, curr_comment_id
                )
            else:
                item = {
                    "name": prop_text[:50],
                    "value": 100,
                    "text": prop_text,
                }
                proposal_data.append(item)

    return proposal_data


def get_comments_text(comments: list):
    comments_text = {}

    for item in comments:
        text = item["text"]
        id = int(item["proposal_id"] if "proposal_id" in item else item["comment_id"])
        if id in comments_text:
            comments_text[id] += text + ". "
        else:
            comments_text[id] = text + ". "

    return comments_text


def get_comment_text(comments_text: dict, id: int, size: int = 10000):
    text = comments_text[id].strip()
    text = text.replace("..", ".")
    text = text.replace("  ", " ")
    text = text[:size]
    return text


def read_comment_hierarchy(input_path: str):
    hierarchy = {}
    file_path = f"{input_path}/comment_hierarchy.csv"
    data = pd.read_csv(file_path, delimiter=",")

    for index, row in data.iterrows():
        proposal_id = row["proposalId"]
        comment_id = row["commendId"]
        parent_id = row["parentId"]

        if proposal_id not in hierarchy:
            hierarchy[proposal_id] = {"comment_ids": [], "parent_ids": []}
        hierarchy[proposal_id]["comment_ids"].append(comment_id)
        hierarchy[proposal_id]["parent_ids"].append(parent_id)

    print(data.head(10))
    return hierarchy


def main():
    solution_path = "C:/Dev Projects/dgov-visual-analytics"
    input_path = f"{solution_path}/data/raw_data"
    proposal_list = ul.read_jsonl_data(input_path)
    hierarchy = read_comment_hierarchy(input_path)
    print(f"Number of files: {len(proposal_list)}")

    for prop_name, prop_data in proposal_list.items():
        if prop_name != "152":
            continue

        comments_text = get_comments_text(prop_data)

        json_data = create_proposal_data(
            prop_name, hierarchy[int(prop_name)], comments_text
        )

        output_file = f"{solution_path}/result/json_data/{prop_name}.json"
        ul.save_dict_to_json(output_file, json_data, 2)


#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    main()
#####################
#### END PROGRAM ####
#####################
