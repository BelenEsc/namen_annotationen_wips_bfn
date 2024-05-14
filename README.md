Autorin und Ansprechpartenerin: Belen Escobari (NFDI4Biodiversity ZE Botanischer Garten und Botanisches Museum)

Kontakt: b.escobari@bo.berlin

# namen_annotationen_wips_bfn
Dieses Repository enthält die Skripte zum Erfassen von Taxon-Namen mit Daten aus den BfN Checklisten

Die Benutzeroberfläche (UI) der API ist unter folgendem Link verfügbar:
https://checklisten.rotelistezentrum.de/api/public/swagger-ui

Die Skripte sind in Python 3.12.0 verfasst

Was benötigt wird:
- Das Skript name_annotations_with_bfn.py (im Repository).
- Das Skript wiki_files.py (im Repository).
- Eine Liste als .txt Datei mit allen Taxon-Namen (ein Beispiel findet sich im Repository als "example_lis.txt". Der Name der Datei muss vom Benutzer  im ersten Script in Zeile 10 angepasst werden). Wenn die Liste einen Header enthalten sollte, muss die Zeile 37 einkommentiert werden.

Der Path ist mit os.path.dirname(os.path.abspath(__file__)) definiert. Daher müssen lediglich die Variablen für die Eingabeliste angepasst werden.

Das Skript name_annotations_with_bfn.py kann in vier Schritte unterteilt werden: 

1. Normalisierung der Namen:
   * Der erste Buchstabe wird großgeschrieben (wie von der API gefordert).
2. Abfrage an die API mit "taxon-by-name": 
   * Die Namen werden einzeln in die API mit taxon-by-name abgefragt.
     
   Als Ausgabe dieses Schrittes wird eine temporäre JSON-Datei mit Daten (u.a. taxon_id) für jeden Namen erzeugt.
   * Aus dieser temporären JSON-Datei werden die "taxon_ids" extrahiert und aufgelistet.
3. Abfrage an die API mit taxon id:
   * Taxon IDs werden einzeln in die API mit "taxon/{id}" gesucht.

   Als Ausgabe wird eine JSON-Datei mit "status", "taxon_id" und "synonyms" für allen Namen insgesammt erstellt   
4. Temporäre Dateien werden gelöscht

Das Skript wiki_files.py erzeugt aus der im letzten Skript generierten Datei einzelne Dateien im MediaWiki-Format für jeden Namen.

