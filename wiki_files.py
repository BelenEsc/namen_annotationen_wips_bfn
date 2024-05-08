import json
import os.path

# Define path
path = os.path.dirname(os.path.abspath(__file__))

# Define input file 
input_file = path + r'\output_full_taxon_wips.json'

# Read JSON
with open (input_file, 'r') as input:
    json_input = json.load(input)
    
for key, value in json_input.items():
    file_name = value["accepted-name"]
    output_file= path + f'\\{file_name}.wiki' 
    name_id = value["id"]
    name_status = value["taxon_status"]
    wiki_text = f"''{file_name}''\n*BfN_Checklist_id: {name_id}\n*name_status: {name_status}\n"

    # Add the synonyms
    if "synonyms" in value:
        wiki_text += f"*synonyms:\n"
        synonyms_list = value['synonyms']
        for value2 in synonyms_list:
            synonyms = value2["name"]
            wiki_text += f"**'{synonyms}'\n"
            
    # Create an output file for each name 
    with open (output_file, "w", encoding='utf-8') as output:
        output.write(wiki_text)
    