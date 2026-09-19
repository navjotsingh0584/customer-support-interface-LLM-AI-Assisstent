from app.services.document_loader import DocumentLoader

loader = DocumentLoader()

documents = loader.load_documents()

print("\nRESULT:")
print("=" * 60)

for doc in documents:
    print(f"Source: {doc['source']}")
    print(f"Length: {len(doc['content'])}")
    print("Preview:")
    print(doc["content"][:200])
    print("=" * 60)