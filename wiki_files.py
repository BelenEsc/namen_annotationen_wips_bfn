from datetime import datetime
import json
import os.path
import re
import argparse, sys

api_url_checklist = "https://checklisten.rotelistezentrum.de/api/public/1/checklist/"  # ids
api_url_taxon = "https://checklisten.rotelistezentrum.de/api/public/1/taxon/"
# Define working_directory
working_directory = os.path.dirname(os.path.abspath(__file__))

# Define input data file
input_data_file = r'output_full_taxon_wips.json'

parser = argparse.ArgumentParser(
    description='Write Wiki text files as results based from previous JSON data checklist query')
parser.add_argument(
    'input_data_file',
    nargs='?',
    default=input_data_file,
    help='the JSON checklist data file to process (default: {default})'.format(default=input_data_file)
)

# Parse the arguments
command_args = parser.parse_args()

print(f"Reading data file {command_args.input_data_file} …")
# sys.exit(0)

input_data_file_path = os.path.join(working_directory, input_data_file)

# Read JSON
with open(command_args.input_data_file, 'r') as thisdata:
    taxon_data = json.load(thisdata)


def translate_taxon_status(status):

    match status.lower():
        case "accepted":
            return "anerkannt"
        case _:
            return status

def format_species_name(scientific_name):
    """
    Return species name in wiki code format, e.g.:
    Acer pseudoplatanus L.
    → ''Acer pseudoplatanus'' L.
    Sorbus × ambigua
    → ''Sorbus'' × ''ambigua''
    Saxifraga rosacea subsp. sponhemica (C. C. Gmel.) D. A. Webb
    → ''Saxifraga rosacea'' subsp. ''sponhemica'' (C. C. Gmel.) D. A. Webb

    @param scientific_name: a word without spaces
    @return: str an abbreviated word
    """

    # single upper case letter in unicode
    # see https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3Aupper%3A%5D&abb=on&ucd=on&esc=on&g=0000000&i=
    uppercase_unicode_letter = r"[A-Z\u00C0-\u00D6\u00D8-\u00DE\u0100\u0102\u0104\u0106\u0108\u010A\u010C\u010E\u0110\u0112" \
                       r"\u0114\u0116\u0118\u011A\u011C\u011E\u0120\u0122\u0124\u0126\u0128\u012A\u012C\u012E\u0130" \
                       r"\u0132\u0134\u0136\u0139\u013B\u013D\u013F\u0141\u0143\u0145\u0147\u014A\u014C\u014E\u0150" \
                       r"\u0152\u0154\u0156\u0158\u015A\u015C\u015E\u0160\u0162\u0164\u0166\u0168\u016A\u016C\u016E" \
                       r"\u0170\u0172\u0174\u0176\u0178\u0179\u017B\u017D\u0181\u0182\u0184\u0186\u0187\u0189-\u018B" \
                       r"\u018E-\u0191\u0193\u0194\u0196-\u0198\u019C\u019D\u019F\u01A0\u01A2\u01A4\u01A6\u01A7\u01A9" \
                       r"\u01AC\u01AE\u01AF\u01B1-\u01B3\u01B5\u01B7\u01B8\u01BC\u01C4\u01C7\u01CA\u01CD\u01CF\u01D1" \
                       r"\u01D3\u01D5\u01D7\u01D9\u01DB\u01DE\u01E0\u01E2\u01E4\u01E6\u01E8\u01EA\u01EC\u01EE\u01F1" \
                       r"\u01F4\u01F6-\u01F8\u01FA\u01FC\u01FE\u0200\u0202\u0204\u0206\u0208\u020A\u020C\u020E\u0210" \
                       r"\u0212\u0214\u0216\u0218\u021A\u021C\u021E\u0220\u0222\u0224\u0226\u0228\u022A\u022C\u022E" \
                       r"\u0230\u0232\u023A\u023B\u023D\u023E\u0241\u0243-\u0246\u0248\u024A\u024C\u024E\u0370\u0372" \
                       r"\u0376\u037F\u0386\u0388-\u038A\u038C\u038E\u038F\u0391-\u03A1\u03A3-\u03AB\u03CF\u03D2-\u03D4" \
                       r"\u03D8\u03DA\u03DC\u03DE\u03E0\u03E2\u03E4\u03E6\u03E8\u03EA\u03EC\u03EE\u03F4\u03F7\u03F9" \
                       r"\u03FA\u03FD-\u042F\u0460\u0462\u0464\u0466\u0468\u046A\u046C\u046E\u0470\u0472\u0474\u0476" \
                       r"\u0478\u047A\u047C\u047E\u0480\u048A\u048C\u048E\u0490\u0492\u0494\u0496\u0498\u049A\u049C" \
                       r"\u049E\u04A0\u04A2\u04A4\u04A6\u04A8\u04AA\u04AC\u04AE\u04B0\u04B2\u04B4\u04B6\u04B8\u04BA" \
                       r"\u04BC\u04BE\u04C0\u04C1\u04C3\u04C5\u04C7\u04C9\u04CB\u04CD\u04D0\u04D2\u04D4\u04D6\u04D8" \
                       r"\u04DA\u04DC\u04DE\u04E0\u04E2\u04E4\u04E6\u04E8\u04EA\u04EC\u04EE\u04F0\u04F2\u04F4\u04F6" \
                       r"\u04F8\u04FA\u04FC\u04FE\u0500\u0502\u0504\u0506\u0508\u050A\u050C\u050E\u0510\u0512\u0514" \
                       r"\u0516\u0518\u051A\u051C\u051E\u0520\u0522\u0524\u0526\u0528\u052A\u052C\u052E\u0531-" \
                       r"\u0556\u10A0-\u10C5\u10C7\u10CD\u13A0-\u13F5\u1C90-\u1CBA\u1CBD-\u1CBF\u1E00\u1E02\u1E04" \
                       r"\u1E06\u1E08\u1E0A\u1E0C\u1E0E\u1E10\u1E12\u1E14\u1E16\u1E18\u1E1A\u1E1C\u1E1E\u1E20\u1E22" \
                       r"\u1E24\u1E26\u1E28\u1E2A\u1E2C\u1E2E\u1E30\u1E32\u1E34\u1E36\u1E38\u1E3A\u1E3C\u1E3E\u1E40" \
                       r"\u1E42\u1E44\u1E46\u1E48\u1E4A\u1E4C\u1E4E\u1E50\u1E52\u1E54\u1E56\u1E58\u1E5A\u1E5C\u1E5E" \
                       r"\u1E60\u1E62\u1E64\u1E66\u1E68\u1E6A\u1E6C\u1E6E\u1E70\u1E72\u1E74\u1E76\u1E78\u1E7A\u1E7C" \
                       r"\u1E7E\u1E80\u1E82\u1E84\u1E86\u1E88\u1E8A\u1E8C\u1E8E\u1E90\u1E92\u1E94\u1E9E\u1EA0\u1EA2" \
                       r"\u1EA4\u1EA6\u1EA8\u1EAA\u1EAC\u1EAE\u1EB0\u1EB2\u1EB4\u1EB6\u1EB8\u1EBA\u1EBC\u1EBE\u1EC0" \
                       r"\u1EC2\u1EC4\u1EC6\u1EC8\u1ECA\u1ECC\u1ECE\u1ED0\u1ED2\u1ED4\u1ED6\u1ED8\u1EDA\u1EDC\u1EDE" \
                       r"\u1EE0\u1EE2\u1EE4\u1EE6\u1EE8\u1EEA\u1EEC\u1EEE\u1EF0\u1EF2\u1EF4\u1EF6\u1EF8\u1EFA\u1EFC" \
                       r"\u1EFE\u1F08-\u1F0F\u1F18-\u1F1D\u1F28-\u1F2F\u1F38-\u1F3F\u1F48-\u1F4D\u1F59\u1F5B\u1F5D" \
                       r"\u1F5F\u1F68-\u1F6F\u1FB8-\u1FBB\u1FC8-\u1FCB\u1FD8-\u1FDB\u1FE8-\u1FEC\u1FF8-\u1FFB\u2102" \
                       r"\u2107\u210B-\u210D\u2110-\u2112\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D" \
                       r"\u2130-\u2133\u213E\u213F\u2145\u2160-\u216F\u2183\u24B6-\u24CF\u2C00-\u2C2F\u2C60\u2C62-\u2C64" \
                       r"\u2C67\u2C69\u2C6B\u2C6D-\u2C70\u2C72\u2C75\u2C7E-\u2C80\u2C82\u2C84\u2C86\u2C88\u2C8A\u2C8C" \
                       r"\u2C8E\u2C90\u2C92\u2C94\u2C96\u2C98\u2C9A\u2C9C\u2C9E\u2CA0\u2CA2\u2CA4\u2CA6\u2CA8\u2CAA" \
                       r"\u2CAC\u2CAE\u2CB0\u2CB2\u2CB4\u2CB6\u2CB8\u2CBA\u2CBC\u2CBE\u2CC0\u2CC2\u2CC4\u2CC6\u2CC8" \
                       r"\u2CCA\u2CCC\u2CCE\u2CD0\u2CD2\u2CD4\u2CD6\u2CD8\u2CDA\u2CDC\u2CDE\u2CE0\u2CE2\u2CEB\u2CED" \
                       r"\u2CF2\uA640\uA642\uA644\uA646\uA648\uA64A\uA64C\uA64E\uA650\uA652\uA654\uA656\uA658\uA65A" \
                       r"\uA65C\uA65E\uA660\uA662\uA664\uA666\uA668\uA66A\uA66C\uA680\uA682\uA684\uA686\uA688\uA68A" \
                       r"\uA68C\uA68E\uA690\uA692\uA694\uA696\uA698\uA69A\uA722\uA724\uA726\uA728\uA72A\uA72C\uA72E" \
                       r"\uA732\uA734\uA736\uA738\uA73A\uA73C\uA73E\uA740\uA742\uA744\uA746\uA748\uA74A\uA74C\uA74E" \
                       r"\uA750\uA752\uA754\uA756\uA758\uA75A\uA75C\uA75E\uA760\uA762\uA764\uA766\uA768\uA76A\uA76C" \
                       r"\uA76E\uA779\uA77B\uA77D\uA77E\uA780\uA782\uA784\uA786\uA78B\uA78D\uA790\uA792\uA796\uA798" \
                       r"\uA79A\uA79C\uA79E\uA7A0\uA7A2\uA7A4\uA7A6\uA7A8\uA7AA-\uA7AE\uA7B0-\uA7B4\uA7B6\uA7B8\uA7BA" \
                       r"\uA7BC\uA7BE\uA7C0\uA7C2\uA7C4-\uA7C7\uA7C9\uA7D0\uA7D6\uA7D8\uA7F5\uFF21-\uFF3A\U00010400-" \
                       r"\U00010427\U000104B0-\U000104D3\U00010570-\U0001057A\U0001057C-\U0001058A\U0001058C-" \
                       r"\U00010592\U00010594\U00010595\U00010C80-\U00010CB2\U000118A0-\U000118BF\U00016E40-" \
                       r"\U00016E5F\U0001D400-\U0001D419\U0001D434-\U0001D44D\U0001D468-\U0001D481\U0001D49C" \
                       r"\U0001D49E\U0001D49F\U0001D4A2\U0001D4A5\U0001D4A6\U0001D4A9-\U0001D4AC\U0001D4AE-" \
                       r"\U0001D4B5\U0001D4D0-\U0001D4E9\U0001D504\U0001D505\U0001D507-\U0001D50A\U0001D50D-" \
                       r"\U0001D514\U0001D516-\U0001D51C\U0001D538\U0001D539\U0001D53B-\U0001D53E\U0001D540-" \
                       r"\U0001D544\U0001D546\U0001D54A-\U0001D550\U0001D56C-\U0001D585\U0001D5A0-" \
                       r"\U0001D5B9\U0001D5D4-\U0001D5ED\U0001D608-\U0001D621\U0001D63C-\U0001D655\U0001D670-" \
                       r"\U0001D689\U0001D6A8-\U0001D6C0\U0001D6E2-\U0001D6FA\U0001D71C-\U0001D734\U0001D756-" \
                       r"\U0001D76E\U0001D790-\U0001D7A8\U0001D7CA\U0001E900-\U0001E921\U0001F130-\U0001F149" \
                       r"\U0001F150-\U0001F169\U0001F170-\U0001F189]"
    # uppercase_unicode_letters = fr"{uppercase_unicode_letter}+"

    if len(scientific_name) > 0:
        names_regex_substitution = {
            # generic simple names: Athyrium filix-femina
            r"^([A-Z][\w]+) +([\w-]+)$": r"''\1 \2''",
            # names Atriplex calotheca (Rafn) Fr.
            r"^([A-Z][\w]+) +([\w-]+) +(\([^\n()]+\)[^\n]*)$": r"''\1 \2'' \3",
            # Acer pseudoplatanus L.
            r"^([A-Z][\w]+) +([\w-]+) +({upper_unicode}[^\n]+)$".format(
                upper_unicode=uppercase_unicode_letter
                ): r"''\1 \2'' \3",

            # Sorbus × ambigua
            r"^([A-Z][\w]+) *([×]) *([\w-]+)$": r"''\1'' \2 ''\3''",
            r"^([A-Z][\w]+) +([x]) +([\w-]+)$": r"''\1'' \2 ''\3''",

            # subsp. case: Rubus gracilis subsp. gracilis
            r"^([A-Z][\w]+) +([\w-]+) +(subsp[.]) +([\w-]+)$": r"''\1 \2'' \3 ''\4''",
            # subsp. case: Biscutella laevigata subsp. gracilis Mach.-Laur.
            r"^([A-Z][\w]+) +([\w-]+) +(subsp[.]) +([\w-]+) +({upper_unicode}[^\n()]+)$".format(
                upper_unicode=uppercase_unicode_letter
                ): r"''\1 \2'' \3 ''\4'' \5",
            # subsp. case: Saxifraga rosacea subsp. sponhemica (C. C. Gmel.) D. A. Webb
            r"^([A-Z][\w]+) +([\w-]+) +(subsp[.]) +([\w-]+) +(\({upper_unicode}[^\n]+)$".format(
                upper_unicode=uppercase_unicode_letter
                ): r"''\1 \2'' \3 ''\4'' \5",
            # subsp. case: Festuca psammophila (Čelak.) Fritsch subsp. psammophila
            r"^([A-Z][\w]+) +([\w-]+) +(\([^()]+\).+ subsp[.]) +([\w-]+)$": r"''\1 \2'' \3 ''\4''",
            # TODO add further name cases and check proper matching of names
        }
        scientific_name = scientific_name.strip()

        for k_search_pattern, v_replace_pattern in names_regex_substitution.items():
            if re.match(k_search_pattern, scientific_name, re.MULTILINE):
                return re.sub(k_search_pattern, v_replace_pattern, scientific_name)
        return scientific_name
    else:
        return scientific_name


print("Write Wiki template files *.wiki ...")
for key_taxon_id, this_datavalue in taxon_data.items():
    # key of ….items() is probably the taxon ID
    output_file = os.path.join(working_directory, '{file_name}.wiki'.format(file_name=this_datavalue["accepted_name"]))
    accepted_name = this_datavalue["accepted_name"]
    # name_id = this_datavalue["id"]
    # name_status = this_datavalue["taxon_status"]
    # TODO check format_species_name(name)
    #  eg. Atriplex calotheca (Rafn) Fr. → ''Atriplex calotheca'' (Rafn) Fr. OR
    #  eg. Biscutella laevigata subsp. gracilis Mach.-Laur. → ''Biscutella laevigata'' subsp. ''gracilis'' Mach.-Laur.
    #  aso.
    # TODO there are kind:consyn (?conceptual synonyms?) and kind:synonym (true synonyms) and to discriminate both
    # use a wiki template to map data, source aso.
    this_synonym_list = []
    wiki_text_de_list = []
    this_consyn_list = []
    this_checklist_citation_list = []
    if "synonyms" in this_datavalue:
        # wiki_text_de += f"* Synonyme:\n"
        # synonyms_list = this_datavalue['synonyms']
        for this_synonym in this_datavalue['synonyms']:
            if this_synonym['kind'] == "synonym":
                this_synonym_list.append(format_species_name(this_synonym["name"]))
            elif this_synonym['kind'] == "consyn":
                this_consyn_list.append(format_species_name(this_synonym["name"]))

    try:
        this_checklist_citation = this_datavalue['checklist_citations'][0]['long_citation']
    except KeyError:
        this_checklist_citation = "?Quellenangabe verfehlt: ?checklist_citations?"

    wiki_text_de_list.append(
        "{{{{Artangaben BfN Prüfliste"
        "\n|wissenschaftlicher Name={accepted_name}"
        "\n|Bearbeitungsstand={name_status}"
        "\n|Datenquelle={checklist_name}, Datenquelle: {wiki_checklist_uri}, {wiki_api_taxon_uri}"
        "\n|Quellenangabe={checklist_citation}"
        "\n|Abfragedatum={query_date}"
        "\n|Synonymliste={names_synonym}"
        "\n|Konzept-Synonymliste={names_consyn}"
        "\n}}}}\n".format(
            accepted_name=format_species_name(accepted_name),
            query_date='{dt.day}.{dt.month}.{dt.year}'.format(dt=datetime.today()),
            # wiki_checklist_uri=this_datavalue['checklist_uri'],
            wiki_checklist_uri="[{uri} {uri_display}]".format(
                uri=this_datavalue['checklist_uri'],
                uri_display=this_datavalue['checklist_uri'].replace("https://", "")
            ),
            # wiki_api_taxon_uri='{api_url_taxon}{taxon_id}'.format(
            #     api_url_taxon=api_url_taxon,
            #     taxon_id=this_datavalue['id']
            # ),
            wiki_api_taxon_uri='[{api_url_taxon}{taxon_id} {api_url_taxon_display}{taxon_id}]'.format(
                api_url_taxon=api_url_taxon,
                api_url_taxon_display=api_url_taxon.replace("https://", ""),
                taxon_id=this_datavalue['id']
            ),
            checklist_name=this_datavalue['checklist'],
            checklist_citation=this_checklist_citation,
            name_status=translate_taxon_status(this_datavalue["taxon_status"]),
            names_synonym="; ".join(this_synonym_list),
            names_consyn="; ".join(this_consyn_list)
        )
    )
    with open(output_file, "a", encoding='utf-8') as output:
        output.write("".join(wiki_text_de_list))

# Create an output file for each name
try:
    output_file
except NameError:
    output_file = os.path.join(working_directory, '{file_name}.wiki'.format(file_name="missing query data"))
    print("Well, we have missing query data somehow. Please check this python code, the API, "
          "or read what basic results are contained in “{output}”!".format(output=output_file))

