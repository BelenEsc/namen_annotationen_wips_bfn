# namen_annotationen_wips_bfn
Dieses Repository enthält die Scripts um Taxon Namen mit Daten aus den BfN Checklisten
UI der API: https://checklisten.rotelistezentrum.de/api/public/swagger-ui

Die Scripts sind in Python 3.12.0 

was man braucht:
- Script name_annotations_with_bfn.py (im Repository)
- Script wiki_files.py (im Repository)
- eine Liste als .txt mit allen Taxon Namen (von Nutzer)

Der Path ist mit os.path.dirname(os.path.abspath(__file__)) definiert. Daher muss man lediglich die Variablen von Input Files in den Scripts anpassen.

Der Script name_annotations_with_bfn.py kan man in vier Schritte beschreiben: 
1. Namen Normalisierung
   * Der erste Buchstabe wird großgeschrieben
   * Da die API keine Autoren berücksichtigt, werden sie aus den Namen gelöscht
2. Abfrage an die API mit Taxon by Name 
   * Namen werden einzeln in die API mit taxon-by-name abgefragt
   Als Output dieses Schrittes wird ein JSON temporäre Datei mit Daten für jeden Namen erzeugt
   * Aus disem temporäre JSON Datei werden die taxon_ids extrahiert und aufgelistet
3. Abfrage an die API mit Taxon ID
   * Taxon IDs werde einzeln in die API mit taxon/{id} gesucht
   Als Output wird ein JSON Datei mit Status, Id, Synonyme u.a. für allen Namen insgesammt erstellt   
4. Temporäre Datein werden gelöscht

Der Script wiki_files.py erzeugt aus dem im letzten Script generierten Datei einzelnen Dateien in MediaWiki Format für jeden Name

