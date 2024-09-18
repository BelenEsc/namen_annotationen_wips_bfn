import urllib

import requests
import json
import time
import os, sys
import argparse
from datetime import timedelta

##### Variables

# Define input list 
# Adjust the name of your file here. Change the "example_list.txt" to the name of your file
# TODO check add file as command line argument to ovewrite default
input_list = 'example_list.txt'
# Define working_directory
working_directory = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(
    description='Query checklist data from https://checklisten.rotelistezentrum.de/api/public/swagger-ui '
                 'based on a text list of taxon names')
parser.add_argument(
    'taxonlist',
    nargs='?',
    default=input_list,
    help='a text list of taxon names (default: {default})'.format(default=input_list)
)

# Parse the arguments
command_args = parser.parse_args()

print(f"Reading taxon names from {command_args.taxonlist} …")
# sys.exit(0)

# Defined urls
api_url_taxon_by_name = "https://checklisten.rotelistezentrum.de/api/public/1/taxa_by_name"  # taxa-by-name
api_url_taxon = "https://checklisten.rotelistezentrum.de/api/public/1/taxon/"  # ids


input_names_list = os.path.join(working_directory, command_args.taxonlist)
# input_names_list = working_directory + f"\\{input_list}"
input_id_list = os.path.join(working_directory, r"taxon_id_wips.txt")
# input_id_list = working_directory + r"\taxon_id_wips.txt"

# Defined output files 
output_taxa_by_name_file = os.path.join(working_directory, r"output_taxa_by_name_wips.json")
output_id_file = os.path.join(working_directory, r"output_full_taxon_wips.json")
taxon_id_file = os.path.join(working_directory, r"taxon_id_wips.txt")
log_file = os.path.join(working_directory, r"error.log")

# Temp variables
taxon_ids_temp = []
output_data_temp = {}

# Capture the start time
start_time = time.time() 

# Read the input file 
with open(input_names_list, 'r') as file:
   # next(file) # ignore the header
    inputlist = []
    for line in file:
        line = line.strip()
        if len(line) > 0:
            inputlist.append (line)


print('Normalize and query names …')
with open(output_taxa_by_name_file, "w") as output_file:
    all_taxnames = []
    for taxname in inputlist:
        taxname = taxname[0].upper() + taxname[1:]
        # taxname = urllib.parse.quote(taxname[0].upper() + taxname[1:])
        params = {
            'taxname': taxname,
            'kingdom': 'plants'
            #'checklists': 43
        }
        
        # send request
        response_taxon_by_name_api = requests.get(api_url_taxon_by_name, params=params)
        # print(vars(response_taxon_by_name_api))
        # print(response_taxon_by_name_api.text)
        if response_taxon_by_name_api.status_code == 200:
            response_text = response_taxon_by_name_api.text
            data = json.loads(response_text)            
            all_taxnames.extend(data['taxnames'])
            if len(data['taxnames'])==0:
                wiki_log = f"Data result for taxon name '{taxname}' is empty." \
                        f" Status code: {response_taxon_by_name_api.status_code};" \
                        f" url {response_taxon_by_name_api.url}. Somthing is not right.\n"
                with open(log_file, "a") as output_log_file:
                    output_log_file.write(wiki_log)

        else:
            wiki_log = f"Failed to retrieve data for taxon name '{taxname}'." \
                       f" Status code: {response_taxon_by_name_api.status_code};" \
                       f" url {response_taxon_by_name_api.url}\n"

            with open(log_file, "a") as output_log_file:
                output_log_file.write(wiki_log)

    # Write JSON output file
    json.dump({"taxnames": all_taxnames}, output_file, indent=4, sort_keys=True)

# Create a temp names-IDs file  
with open(output_taxa_by_name_file, 'r') as file:
    data = json.load(file)
    for taxname in data['taxnames']:
        taxon_ids_temp.append(taxname['taxon_id'])

with open(taxon_id_file, 'w') as output_file:
    for taxon_id in taxon_ids_temp:
        output_file.write(f"{taxon_id}\n")

# Read the names IDs file 
with open(input_id_list, 'r') as file:
    inputlist = [line.strip() for line in file]

print("Query checklist api …")
for taxon_id in inputlist:
    # Construct the complete URL as string with taxon ID
    url_final_request = api_url_taxon + taxon_id + r"?output-synonyms%3F=true"
        # output-hierarchy%3F=true seems unneeded for just the synonyms

    response2 = requests.get(url_final_request)
    if response2.status_code == 200:
        response_text = response2.text
        data = json.loads(response_text)
        output_data_temp[taxon_id] = data  # Add response to output dictionary
    else:
        # Create a log file with errors
        wiki_log = f"Failed to retrieve data for taxon_ID'{taxon_id}'." \
                   f" Status code: {response2.status_code};" \
                   f" url {response2.url}\n"
        with open(log_file, "a") as output_log_file:
            output_log_file.write(wiki_log)

print("Write JSON data file …")
# Write the output JSON file
with open(output_id_file, 'w') as output_file:
    json.dump(output_data_temp, output_file, indent=4)

# Remove temp files
os.remove(input_id_list)
os.remove(output_taxa_by_name_file)

end_time = time.time() # Capture the end time
execution_time = timedelta(seconds=(end_time - start_time))  # Calculate the elapsed time

print(f'The script took {execution_time} to run.')
if os.path.exists(log_file):
    print(
        f"There are some issues in {log_file}.\n" \
        f"Please check them before you transform the result to Wiki code by running: python wiki_files.py"
    )
else:
    print(f'Now, to get Wiki text from the result, run: python wiki_files.py')
