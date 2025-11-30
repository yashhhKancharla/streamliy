# Commands to Display Vector DB Content

This document provides commands to view and interact with the ChromaDB vector database in this project.

## Quick Command List

### 1. **View Vector DB Statistics (Quickest Way)**

```bash
python -c "
from app.services.chroma_service import ChromaService
service = ChromaService()
stats = service.get_stats()
print('Collection Stats:')
for key, value in stats.items():
    print(f'  {key}: {value}')
"
```

### 2. **List All Ingested Documents**

```bash
python -c "
from app.services.chroma_service import ChromaService
service = ChromaService()
sources = service.list_document_sources()
print(f'Found {len(sources)} document sources:\n')
for doc in sources:
    print(f'  - {doc[\"source\"]} ({doc[\"chunk_count\"]} chunks)')
    print(f'    Category: {doc[\"category\"]}')
    print(f'    Uploaded: {doc[\"uploaded_at\"]}\n')
"
```

### 3. **Query Vector DB and Display Results**

```bash
python -c "
from app.services.chroma_service import ChromaService
service = ChromaService()
results = service.query('authentication', k=5)
print(f'Query: {results[\"query\"]}')
print(f'Total Results: {results[\"total_results\"]}')
print(f'Retrieval Time: {results[\"retrieval_time_ms\"]}ms\n')
for i, result in enumerate(results['results'], 1):
    print(f'{i}. Similarity Score: {result[\"similarity_score\"]}')
    print(f'   Source: {result[\"metadata\"].get(\"source\", \"unknown\")}')
    print(f'   Content: {result[\"content\"][:100]}...\n')
"
```

### 4. **Get All Documents with Full Content**

```bash
python -c "
from app.services.chroma_service import ChromaService
service = ChromaService()
collection = service.collection
count = collection.count()
if count > 0:
    all_docs = collection.get(limit=count, include=['documents', 'metadatas'])
    print(f'Total Documents: {count}\n')
    for i, (doc, meta) in enumerate(zip(all_docs['documents'], all_docs['metadatas']), 1):
        print(f'{i}. Document from {meta.get(\"source\", \"unknown\")}')
        print(f'   Chunk {meta.get(\"chunk_index\", \"?\")} of {meta.get(\"chunk_count\", \"?\")}')
        print(f'   Content: {doc[:150]}...\n')
else:
    print('No documents in database')
"
```

### 5. **Export Vector DB to JSON**

```bash
python -c "
import json
from app.services.chroma_service import ChromaService
service = ChromaService()
collection = service.collection
count = collection.count()
if count > 0:
    all_docs = collection.get(limit=count, include=['documents', 'metadatas', 'embeddings'])
    output = {
        'collection': service.collection_name,
        'total_count': count,
        'documents': []
    }
    for i, (doc, meta, doc_id) in enumerate(zip(all_docs['documents'], all_docs['metadatas'], all_docs['ids'])):
        output['documents'].append({
            'id': doc_id,
            'content': doc,
            'metadata': meta
        })
    with open('vector_db_export.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f'✓ Exported {count} documents to vector_db_export.json')
else:
    print('No documents to export')
"
```

### 6. **Display Database Statistics with Collection Info**

```bash
python -c "
from app.services.chroma_service import ChromaService
import json
service = ChromaService()
stats = service.get_stats()
sources = service.list_document_sources()
print('=== ChromaDB Statistics ===')
print(f'Collection: {stats[\"collection_name\"]}')
print(f'Total Chunks: {stats[\"document_count\"]}')
print(f'Persist Directory: {stats[\"persist_directory\"]}')
print(f'Has Documents: {stats[\"has_documents\"]}')
print(f'\nDocument Sources ({len(sources)}):')
for source in sources:
    print(f'  - {source[\"source\"]}: {source[\"chunk_count\"]} chunks')
"
```

---

## Using the REST API

If your Flask server is running, use these curl commands:

### 7. **List Documents via API**

```bash
curl http://localhost:5000/list-documents
```

### 8. **Query Vector DB via API**

```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "authentication", "k": 5}'
```

### 9. **Get DB Health via API**

```bash
curl http://localhost:5000/health
```

---

## Interactive Python Script

Create a file `view_vector_db.py`:

```python
#!/usr/bin/env python
"""Interactive Vector DB Viewer"""

from app.services.chroma_service import ChromaService
import json

def main():
    service = ChromaService()

    while True:
        print("\n=== Vector DB Viewer ===")
        print("1. View statistics")
        print("2. List document sources")
        print("3. Query database")
        print("4. View all documents")
        print("5. Export to JSON")
        print("0. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            stats = service.get_stats()
            print("\n" + json.dumps(stats, indent=2))

        elif choice == "2":
            sources = service.list_document_sources()
            print(f"\nFound {len(sources)} sources:")
            for doc in sources:
                print(f"  - {doc['source']}: {doc['chunk_count']} chunks")

        elif choice == "3":
            query = input("Enter search query: ")
            k = int(input("Number of results (default 5): ") or "5")
            results = service.query(query, k=k)
            print(f"\nFound {results['total_results']} results in {results['retrieval_time_ms']}ms:")
            for result in results['results']:
                print(f"  - Score: {result['similarity_score']}")
                print(f"    {result['content'][:100]}...")

        elif choice == "4":
            collection = service.collection
            count = collection.count()
            if count > 0:
                all_docs = collection.get(limit=count, include=['documents', 'metadatas'])
                print(f"\nTotal: {count} documents")
                for i, (doc, meta) in enumerate(zip(all_docs['documents'], all_docs['metadatas']), 1):
                    print(f"\n{i}. From {meta.get('source', 'unknown')}")
                    print(f"   {doc[:150]}...")
            else:
                print("\nNo documents in database")

        elif choice == "5":
            collection = service.collection
            count = collection.count()
            if count > 0:
                all_docs = collection.get(limit=count, include=['documents', 'metadatas', 'ids'])
                output = {
                    'collection': service.collection_name,
                    'total_count': count,
                    'documents': []
                }
                for doc, meta, doc_id in zip(all_docs['documents'], all_docs['metadatas'], all_docs['ids']):
                    output['documents'].append({
                        'id': doc_id,
                        'content': doc,
                        'metadata': meta
                    })
                filename = 'vector_db_export.json'
                with open(filename, 'w') as f:
                    json.dump(output, f, indent=2)
                print(f"\n✓ Exported {count} documents to {filename}")
            else:
                print("\nNo documents to export")

        elif choice == "0":
            break

if __name__ == "__main__":
    main()
```

Run with:

```bash
python view_vector_db.py
```

---

## Quick Reference

| Command                                                                                                             | Purpose                               |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `python -c "from app.services.chroma_service import ChromaService; print(ChromaService().get_stats())"`             | Quick stats                           |
| `python -c "from app.services.chroma_service import ChromaService; print(ChromaService().list_document_sources())"` | List documents                        |
| `python view_vector_db.py`                                                                                          | Interactive viewer                    |
| `curl http://localhost:5000/list-documents`                                                                         | API endpoint (server must be running) |

---

## Data Location

Vector DB data is stored at:

```
./data/chroma/         # Main production database
./data/chroma_test/    # Test database
```

Each contains:

- `chroma.sqlite3` - Database file
- `UUID folders` - Embedding storage
