# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.2
    Created on: Nov 23, 2023
    Updated on: Nov 24, 2023
    Description: Generate proposal data.
"""
import util_libs as ul
import pandas as pd

MAX_TEXT_SIZE = 200


def create_proposal_data(proposal_id: int, proposal_hierarchy: dict, comments: dict):
    prop_text = get_comment_text(comments[proposal_id])
    prop_short_text = get_comment_short_text(prop_text)

    proposal_data = {
        "name": str(proposal_id),
        "children": [],
        "text": prop_text,
        "short_text": prop_short_text,
    }
    parent_id = -1

    proposal_data["children"] = __create_proposal_data_inner(
        proposal_data["children"], proposal_hierarchy, comments, parent_id
    )

    return proposal_data


def __create_proposal_data_inner(
    proposal_data: list,
    proposal_hierarchy: dict,
    comments: dict,
    parent_id: int = -1,
):
    comment_ids = proposal_hierarchy["comment_ids"]
    parent_ids = proposal_hierarchy["parent_ids"]

    for curr_comment_id, curr_parent_id in zip(comment_ids, parent_ids):
        if curr_parent_id == parent_id:
            prop_text = get_comment_text(comments[curr_comment_id])
            prop_short_text = get_comment_short_text(prop_text)

            if curr_comment_id in parent_ids:
                item = {
                    "name": str(curr_comment_id),
                    "children": [],
                    "text": prop_text,
                    "short_text": prop_short_text,
                }
                proposal_data.append(item)
                __create_proposal_data_inner(
                    item["children"], proposal_hierarchy, comments, curr_comment_id
                )
            else:
                if len(prop_text) > 0:
                    item = {
                        "name": str(curr_comment_id),
                        "value": 100,
                        "text": prop_text,
                        "short_text": prop_short_text,
                    }
                    proposal_data.append(item)

    return proposal_data


def get_proposal_comments(prop_data: list):
    comments = {}

    for item in prop_data:
        text = item["text"].strip()
        id = int(item["proposal_id"] if "proposal_id" in item else item["comment_id"])
        if id in comments:
            comments[id] += ". " + text
        else:
            comments[id] = text

    return comments


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
    proposals = ul.read_jsonl_data(input_path)
    hierarchy = read_comment_hierarchy(input_path)
    print(f"Number of proposals: {len(proposals)}")

    for prop_name, prop_data in proposals.items():
        prop_id = int(prop_name)

        comments = get_proposal_comments(prop_data)

        json_data = create_proposal_data(prop_id, hierarchy[prop_id], comments)
        n_items = len(json_data["children"])
        print(f"Proposal: {prop_id} and number of items: {n_items}")

        output_file = f"{solution_path}/result/json_data/proposals/{prop_name}.json"
        ul.save_dict_to_json(output_file, json_data, 2)


#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    main()
#####################
#### END PROGRAM ####
#####################
