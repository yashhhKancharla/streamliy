"""
Direct ChromaDB Test - Verify upgrade worked
Tests ChromaDB independently of Flask server
"""

import sys
sys.path.insert(0, '.')

print("Testing ChromaDB after upgrade to 1.3.5...\n")

try:
    # Test 1: Import ChromaDB
    print("1. Importing ChromaDB...")
    import chromadb
    print(f"   ✓ ChromaDB version: {chromadb.__version__}")
    
    # Test 2: Create PersistentClient
    print("\n2. Creating PersistentClient...")
    client = chromadb.PersistentClient(path="./data/chroma_test")
    print("   ✓ Client created successfully")
    
    # Test 3: Create collection
    print("\n3. Creating collection...")
    try:
        collection = client.get_or_create_collection(name="test_collection")
        print(f"   ✓ Collection created: {collection.name}")
    except Exception as e:
        print(f"   ✗ Collection creation failed: {e}")
        sys.exit(1)
    
    # Test 4: Add documents
    print("\n4. Adding test documents...")
    collection.add(
        documents=["This is a test document about authentication"],
        ids=["test_1"]
    )
    print(f"   ✓ Documents added. Collection count: {collection.count()}")
    
    # Test 5: Query
    print("\n5. Querying documents...")
    results = collection.query(
        query_texts=["authentication"],
        n_results=1
    )
    print(f"   ✓ Query successful. Found {len(results['documents'][0])} results")
    if results['documents'][0]:
        print(f"   └─ Result: {results['documents'][0][0][:50]}...")
    
    # Test 6: Clean up
    print("\n6. Cleaning up...")
    client.delete_collection(name="test_collection")
    print("   ✓ Test collection deleted")
    
    print("\n" + "="*60)
    print("✓ All ChromaDB tests passed!")
    print("="*60)
    print("\nChromaDB is working correctly.")
    print("NEXT STEP: Restart your Flask server to use the new ChromaDB version")
    print("Command: Ctrl+C in Flask terminal, then rerun start command")
    
except Exception as e:
    print(f"\n✗ ChromaDB test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
