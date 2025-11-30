#!/usr/bin/env python
"""Interactive Vector DB Viewer - Display ChromaDB content"""

from app.services.chroma_service import ChromaService
import json
import sys

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def view_statistics():
    """Display database statistics"""
    print_header("Database Statistics")
    service = ChromaService()
    stats = service.get_stats()
    sources = service.list_document_sources()
    
    print(f"Collection Name:    {stats['collection_name']}")
    print(f"Total Chunks:       {stats['document_count']}")
    print(f"Persist Directory:  {stats['persist_directory']}")
    print(f"Has Documents:      {stats['has_documents']}")
    print(f"\nUnique Sources:     {len(sources)}")
    
    if sources:
        print("\nDocument Breakdown:")
        total_chunks = 0
        for source in sources:
            chunks = source['chunk_count']
            total_chunks += chunks
            print(f"  • {source['source']:<40} {chunks:>4} chunks")
        print(f"\n{'Total:':<44} {total_chunks:>4} chunks")

def list_document_sources():
    """List all document sources"""
    print_header("Document Sources")
    service = ChromaService()
    sources = service.list_document_sources()
    
    if not sources:
        print("No documents found in database")
        return
    
    print(f"Found {len(sources)} document source(s):\n")
    for i, doc in enumerate(sources, 1):
        print(f"{i}. {doc['source']}")
        print(f"   Category:   {doc['category']}")
        print(f"   Chunks:     {doc['chunk_count']}")
        print(f"   Uploaded:   {doc['uploaded_at']}")
        print()

def query_database():
    """Interactive query"""
    print_header("Query Vector Database")
    query = input("Enter search query: ").strip()
    if not query:
        print("Query cannot be empty")
        return
    
    try:
        k = int(input("Number of results (default 5): ") or "5")
    except ValueError:
        k = 5
    
    service = ChromaService()
    results = service.query(query, k=k)
    
    print(f"\nQuery: '{results['query']}'")
    print(f"Results: {results['total_results']}")
    print(f"Retrieval Time: {results['retrieval_time_ms']}ms\n")
    
    if not results['results']:
        print("No results found")
        return
    
    for i, result in enumerate(results['results'], 1):
        print(f"{i}. Similarity Score: {result['similarity_score']:.4f}")
        print(f"   Source: {result['metadata'].get('source', 'unknown')}")
        print(f"   Chunk: {result['metadata'].get('chunk_index', '?')} of {result['metadata'].get('chunk_count', '?')}")
        print(f"   Content Preview:")
        content = result['content']
        lines = content.split('\n')
        for line in lines[:3]:
            if line.strip():
                print(f"     {line[:70]}...")
        if len(lines) > 3:
            print(f"     ... ({len(lines)} lines total)")
        print()

def view_all_documents():
    """Display all documents"""
    print_header("All Documents in Database")
    service = ChromaService()
    collection = service.collection
    count = collection.count()
    
    if count == 0:
        print("No documents in database")
        return
    
    print(f"Total Documents: {count}\n")
    
    all_docs = collection.get(limit=count, include=['documents', 'metadatas'])
    
    for i, (doc, meta) in enumerate(zip(all_docs['documents'], all_docs['metadatas']), 1):
        print(f"{i}. From: {meta.get('source', 'unknown')}")
        print(f"   Chunk {meta.get('chunk_index', '?')} of {meta.get('chunk_count', '?')}")
        print(f"   Content ({len(doc)} chars):")
        lines = doc.split('\n')
        for line in lines[:5]:
            if line.strip():
                print(f"     {line[:70]}")
        if len(doc) > 350:
            print(f"     ... (truncated)")
        print()
        
        if i >= 10:  # Limit display
            remaining = count - 10
            if remaining > 0:
                print(f"... and {remaining} more documents")
            break

def export_to_json():
    """Export database to JSON"""
    print_header("Export to JSON")
    service = ChromaService()
    collection = service.collection
    count = collection.count()
    
    if count == 0:
        print("No documents to export")
        return
    
    all_docs = collection.get(limit=count, include=['documents', 'metadatas', 'ids'])
    
    output = {
        'collection': service.collection_name,
        'total_count': count,
        'persist_directory': service.persist_directory,
        'documents': []
    }
    
    for doc, meta, doc_id in zip(all_docs['documents'], all_docs['metadatas'], all_docs['ids']):
        output['documents'].append({
            'id': doc_id,
            'content': doc,
            'metadata': meta
        })
    
    filename = 'vector_db_export.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Successfully exported {count} documents")
    print(f"✓ File saved: {filename}")
    print(f"✓ File size: {len(json.dumps(output, indent=2))} bytes")

def view_sample_metadata():
    """View sample metadata"""
    print_header("Sample Metadata")
    service = ChromaService()
    stats = service.get_stats()
    
    if 'sample_metadata' in stats and stats['sample_metadata']:
        print("Sample Metadata from First Document:")
        print(json.dumps(stats['sample_metadata'], indent=2))
    else:
        print("No sample metadata available")

def main():
    """Main menu"""
    print("\n" + "="*60)
    print("  Vector Database Viewer - ChromaDB Inspector")
    print("="*60)
    
    options = {
        '1': ('View Statistics', view_statistics),
        '2': ('List Document Sources', list_document_sources),
        '3': ('Query Database', query_database),
        '4': ('View All Documents', view_all_documents),
        '5': ('View Sample Metadata', view_sample_metadata),
        '6': ('Export to JSON', export_to_json),
        '0': ('Exit', None)
    }
    
    while True:
        print("\n" + "="*60)
        print("  Menu Options")
        print("="*60)
        for key, (label, _) in options.items():
            print(f"  {key}. {label}")
        print("="*60)
        
        choice = input("\nSelect option (0-6): ").strip()
        
        if choice not in options:
            print("Invalid option. Please try again.")
            continue
        
        label, func = options[choice]
        
        if choice == '0':
            print("\nGoodbye!")
            break
        
        try:
            func()
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
