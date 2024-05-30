Autoren und Ansprechpartener: 
* Belen Escobari (b.escobari@bo.berlin, NFDI4Biodiversity, ZE Botanischer Garten und Botanisches Museum)
* Andreas Plank (a.plank@bo.berlin, WIPs-De (bot. Wildpflanzenschutz Deutschland), ZE Botanischer Garten und Botanisches Museum)



# namen_annotationen_wips_bfn
Dieses Repository enthält die Skripte zum Erfassen von Taxon-Namen mit Daten aus den BfN Checklisten

Die Benutzeroberfläche (UI) der API ist unter folgendem Link verfügbar:
https://checklisten.rotelistezentrum.de/api/public/swagger-ui

Die Skripte sind in Python 3.12.0 verfasst

Beispiel-Befehlsaufruf zum Abfragen und Formatieren der Taxon-Namen (falls unter Windows, Befehl `python` mit `python.exe` ersetzen):

```bash
# (0) Befehlshilfe aufrufen
python name_annotations_with_bfn.py --help
 
# (1) Namensliste abfragen und Daten holen
python name_annotations_with_bfn.py # das Skript verwendet die Beispielvorlage example_list.txt
# oder eine gesonderte Textdatei angeben
# python name_annotations_with_bfn.py Verantwortungsarten_Liste_WIPs-Portal.txt

# (2) abgespeicherte Daten durcharbeiten und als Wiki-Text ausgeben
python wiki_files.py --help # Befehlshilfe aufrufen
python wiki_files.py
```

Was benötigt wird:
- Das Skript [`name_annotations_with_bfn.py`](./name_annotations_with_bfn.py) (im Repository).
- Das Skript [`wiki_files.py`](./wiki_files.py) (im Repository).
- Eine Liste als .txt Datei mit allen Taxon-Namen (ein Beispiel findet sich im Repository als “[`example_list.txt`](./example_list.txt)”. Die Taxonliste kann jede beliebige Textdatei sein, z.B. `python name_annotations_with_bfn.py Verantwortungsarten_Liste_WIPs-Portal.txt`

Das Arbeitsverzeichnis ist mit `os.path.dirname(os.path.abspath(__file__))` definiert. Daher müssen lediglich die Variablen für die Eingabeliste angepasst werden.

Das Skript `name_annotations_with_bfn.py` kann in vier Arbeitsschritte unterteilt werden: 

1. Normalisierung der Namen:
   * Der erste Buchstabe wird großgeschrieben (wie von der API gefordert).
2. Namensabfrage vermittels `"taxon-by-name"`-API: 
   * Die Namen werden einzeln in die API mit taxon-by-name abgefragt.
     
   Als Ausgabe dieses Schrittes wird eine temporäre JSON-Datei mit Daten (u.a. `"taxon-id"`) für jeden Namen erzeugt.
   * Aus dieser temporären JSON-Datei werden die "taxon_ids" extrahiert und aufgelistet.
3. Abfrage an die API mit den `id` der Taxa:
   * Taxon IDs werden einzeln in die API mit `"taxon/{id}"` gesucht.

   Als Ausgabe wird eine JSON-Datei mit `"status"`, `"taxon_id"` und `"synonyms"` aller Namen insgesamt erstellt   
4. Temporäre Dateien werden gelöscht

Das Skript [`wiki_files.py`](./wiki_files.py) erzeugt aus der im letzten Skript generierten Datei einzelne Dateien im MediaWiki-Format für jeden Namen, in Form einer Wiki-Text-Vorlage.

