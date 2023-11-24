# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.2
    Created on: Nov 24, 2023
    Updated on: Nov 24, 2023
    Description: Generate network data.
"""

import util_libs as ul


def create_argument_data(proposal_id: int, arg_data: dict):
    proposal_name = f"proposal {proposal_id}"
    nodes = [{"id": proposal_name, "group": 0}]
    links = []

    for key, value in arg_data.items():
        # Create root node
        node = {"id": key, "group": -3}
        nodes.append(node)
        link = {"source": proposal_name, "target": key, "value": 1}
        links.append(link)

        # Create support and attack nodes and links
        id = f"{key}_support"
        node = {"id": id, "group": -1}
        nodes.append(node)
        link = {"source": key, "target": id, "value": 2}
        links.append(link)

        id = f"{key}_attack"
        node = {"id": id, "group": -2}
        nodes.append(node)
        link = {"source": key, "target": id, "value": 2}
        links.append(link)

        for arg in value:
            text = arg["arg_description"]
            intent = arg["arg_intent"]

            if intent == "A favor":
                group = -1
                id = f"{key}_support"
            else:
                group = -2
                id = f"{key}_attack"

            node = {"id": text, "group": group}
            nodes.append(node)
            link = {"source": id, "target": text, "value": 3}
            links.append(link)

    network_data = {"nodes": nodes, "links": links}
    return network_data


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
    input_path = f"{solution_path}/data/gpt_data"
    arguments = load_arguments(input_path)
    print(f"Number of arguments: {len(arguments)}")

    for prop_id, arg_data in arguments.items():
        json_data = create_argument_data(prop_id, arg_data)
        print(f"Number of items: {len(json_data)}")

        output_file = f"{solution_path}/result/json_data/networks/{prop_id}.json"
        ul.save_dict_to_json(output_file, json_data, 2)


#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    main()
#####################
#### END PROGRAM ####
#####################
