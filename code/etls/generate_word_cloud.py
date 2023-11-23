# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.1
    Created on: Nov 21, 2023
    Updated on: Nov 23, 2023
    Description: Main class.
"""
import util_libs as ul
from wordcloud import WordCloud
import spacy

# Load the spaCy model for Spanish
nlp = spacy.load("es_core_news_lg")


# Function to extract entities from text
def extract_entities(text):
    doc = nlp(text)
    relevant_entity_types = ["PER", "ORG", "LOC", "GPE", "NORP"]
    entities = [
        f"{ent.text} ({ent.label_ })"
        for ent in doc.ents
        if ent.label_ in relevant_entity_types
    ]
    return list(set(entities))


def generate_and_save_wordcloud(text, output_path):
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )

    # Save word cloud image to the specified folder
    wordcloud.to_file(output_path)


def main():
    solution_path = "C:/Dev Projects/dgov-visual-analytics"
    input_path = f"{solution_path}/data/raw_data"
    proposal_list = ul.read_jsonl_data(input_path)
    print(f"Number of files: {len(proposal_list)}")

    entity_list = []

    for prop_name, prop_data in proposal_list.items():
        # Concatenate the extracted 'text' fields
        prop_text = ul.concatenate_texts_from_jsonl(prop_data, "text")

        # Remove spanish stopwords
        spanish_stopwords = ul.load_stopwords(solution_path, "spanish")
        filtered_words = ul.remove_stopwords(prop_text, spanish_stopwords, 3)

        # Extract entities from the text
        entities = extract_entities(filtered_words)
        entity_list.append([prop_name, entities])

        # Generate and save word cloud
        output_path = f"{solution_path}/result/images/{prop_name}.png"
        generate_and_save_wordcloud(filtered_words, output_path)

    output_path = f"{solution_path}/result/ner/entities.csv"
    columns = ["file", "entities"]
    ul.save_list_to_csv(output_path, columns, entity_list)


#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    main()
#####################
#### END PROGRAM ####
#####################
