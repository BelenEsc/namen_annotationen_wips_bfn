import requests
import json
import time
import os

# Capture the start time
start_time = time.time() 

##### Variables

# Define urls 
url_taxon_by_name = "https://checklisten.rotelistezentrum.de/api/public/1/taxa-by-name?&checklists=43" # taxa-by-name
url_taxon_id = "https://checklisten.rotelistezentrum.de/api/public/1/taxon/" # ids

# Define path
path = os.path.dirname(os.path.abspath(__file__))

# Define input files
input_names_list = path + r"\wips.txt"
input_id_list = path + r"\taxon_id_wips.txt"

# Define output files 
output_taxa_by_name_file = path + r"\output_taxa_by_name_wips.json"
output_id_file = path + r"\output_full_taxon_wips.json"
taxon_id_file = path + r"\taxon_id_wips.txt"
log_file = path + r"\error.log"

# Temp variables
taxon_ids_temp = []
output_data_temp = {}


##### Functions

def delete_authors(input_string):
    parts = input_string.split()
    if 'subsp.' in parts[2]:
        name_without_authors = parts[0] + " " + parts[1] + " " + parts[2] + " " + parts[3]
    else:
        name_without_authors = parts[0] +" "+ parts[1]
    return name_without_authors

# Read the input file 
with open(input_names_list, 'r') as file:
    next(file) # ignore the header
    inputlist = []
    for line in file:
        line = line.strip() 
        inputlist.append (line)


# Normalize names
with open(output_taxa_by_name_file, "w") as output_file:
    all_taxnames = []
    for taxname in inputlist:
        taxname = taxname.capitalize()
        taxname = delete_authors(taxname)            
        params = {'taxname': taxname}
        
        # send request   
        response1 = requests.get(url_taxon_by_name, params=params)
        
        if response1.status_code == 200:
            response_text=response1.text
            data = json.loads(response_text)
            all_taxnames.extend(data['taxnames'])
        else:
                wiki_log = f"Failed to retrieve data for taxon name '{taxname}'. Status code: {response1.status_code}; url {response1.url}\n"
                
                with open(log_file, "a") as output_log_file:
                    output_log_file.write(wiki_log)

    # Write JSON output file
    json.dump({"taxnames": all_taxnames}, output_file, indent=4, sort_keys=True)

# Create a temp names-IDs file  
with open(output_taxa_by_name_file, 'r') as file:
    data = json.load(file)
    for taxname in data['taxnames']:
        taxon_ids_temp.append(taxname['taxon-id'])

with open(taxon_id_file, 'w') as output_file:
    for taxon_id in taxon_ids_temp:
        output_file.write(f"{taxon_id}\n")

# Read the names IDs file 
with open(input_id_list, 'r') as file:
    inputlist = [line.strip() for line in file]

for taxon_id in inputlist:
    # Construct the complete URL as string with taxon ID
    url_final_request = url_taxon_id + taxon_id + r"?output-hierarchy%3F=true&output-synonyms%3F=true"
    response2 = requests.get(url_final_request)
    if response2.status_code == 200:
        response_text = response2.text
        data = json.loads(response_text)
        output_data_temp[taxon_id] = data # Add response to output dictionary
    else:
            # Create a log file with errors 
            wiki_log = f"Failed to retrieve data for taxon_ID'{taxon_id}'. Status code: {response2.status_code}; url {response2.url}\n"
            with open(log_file, "a") as output_log_file:
                output_log_file.write(wiki_log)
    
# Write the output JSON file
with open(output_id_file, 'w') as output_file:
    json.dump(output_data_temp, output_file, indent=4)

# Remove temp files
os.remove(input_id_list)
os.remove(output_taxa_by_name_file)

end_time = time.time() # Capture the end time
execution_time = (end_time - start_time)/60 # Calculate the elapsed time

print(f'The script took {execution_time} min to run.')