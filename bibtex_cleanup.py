import os
import bibtexparser

with open(
    os.path.join(os.path.dirname(__file__), 'zotero.bib')
) as infile:
    bibdb = bibtexparser.load(infile)
    
with open(
    os.path.join(os.path.dirname(__file__), 'mendeley.bib')
) as infile:
    bibdb2 = bibtexparser.load(infile)
    
with open(
    os.path.join(os.path.dirname(__file__), 'clean_ref_cache.bib')
) as infile2:
    cachebibdb = bibtexparser.load(infile2)

    
entry_id_delete = []
cache_id = {entry.get('ID', '') for entry in cachebibdb.entries}
seen_id = set()
logged_refs = set()

print(cache_id)
    
def clean_entries(entries): 
    for entry in entries:
        if 'abstract' in entry:
            del entry['abstract']

        if 'keywords' in entry:
            del entry['keywords']

        if 'language' in entry:
            del entry['language']
            
        try:
            author = entry.get('author', '').split(',')[0].lower() or entry.get('editor', '').split(',')[0].lower()
            author = author.split()[-1]
            year = entry.get('year', '').split()[-1]
            doi = entry.get('doi', '')

            i = 1
            bib_id = f"{author}{year[-2:]}"
            alt_bib_id = bib_id
            while alt_bib_id in seen_id or alt_bib_id in cache_id:
                alt_bib_id = f"{author}{year[-2:]}{chr(ord('a') + i)}"
                i += 1

            if bib_id in seen_id and doi in logged_refs:
                entry_id_delete.append(entry['ID'])
            elif bib_id in seen_id and doi not in logged_refs:
                entry['ID'] = alt_bib_id
            else:
                entry['ID'] = bib_id
                
            if entry['ID'] in cache_id:
                entry_id_delete.append(entry['ID'])

        except:
            entry_id_delete.append(entry['ID'])
            continue

        seen_id.add(entry['ID'])
        logged_refs.add(doi)
        

clean_entries(bibdb.entries)
clean_entries(bibdb2.entries)
        
entry_sorted = sorted([entry for entry in bibdb.entries 
                     if not entry.get('ID') in entry_id_delete] + 
                      [entry for entry in bibdb2.entries 
                     if not entry.get('ID') in entry_id_delete] +
                      [entry for entry in cachebibdb.entries], 
                    key=lambda x: x['ID'])

bibdb_sorted = bibtexparser.bibdatabase.BibDatabase()
bibdb_sorted.entries = entry_sorted

with open(
    os.path.join(os.path.dirname(__file__), 'clean_ref.bib'), 'w'
) as outfile:
    bibtexparser.dump(bibdb_sorted, outfile)

# Comment out for debug
with open(
    os.path.join(os.path.dirname(__file__), 'clean_ref_cache.bib'), 'w'
) as outfile2:
    bibtexparser.dump(bibdb_sorted, outfile2)