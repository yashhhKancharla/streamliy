#!/bin/bash

# Ingest documentation into ChromaDB
# Grounded_In: Assignment - 1.pdf

echo "📚 Ingesting documentation..."

# Load environment
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Activate venv if exists
if [ -d "venv" ]; then
    source venv/bin/activate || . venv/Scripts/activate
fi

# Run ingestion script
python3 << 'EOF'
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path.cwd()))

from app.services.chroma_service import ingest_from_files

# Get all documentation files
docs_dir = Path("docs")
if not docs_dir.exists():
    print("❌ docs/ directory not found")
    sys.exit(1)

doc_files = list(docs_dir.glob("*.md")) + list(docs_dir.glob("*.json"))

if not doc_files:
    print("❌ No documentation files found")
    sys.exit(1)

print(f"📄 Found {len(doc_files)} documentation files:")
for file in doc_files:
    print(f"  - {file.name}")

# Ingest files
print("\n🔄 Ingesting documents...")
result = ingest_from_files([str(f) for f in doc_files])

print(f"\n✅ Ingestion complete!")
print(f"  Documents: {result['ingested_count']}")
print(f"  Chunks: {result['chunks_created']}")
print(f"  Time: {result['processing_time_ms']}ms")
print(f"  Collection: {result['collection']}")
EOF

echo "✅ Documentation ingested successfully"
