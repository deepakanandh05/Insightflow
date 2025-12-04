from llama_index.core import VectorStoreIndex


def create_or_load_vector_index(
    embed_model,
    parser,
    storage_context,
    vector_store,
    nodes,
    collection_name,
    company_name,
):
    """
    Create or load a Milvus vector index safely.
    - Adds company_name metadata to each node.
    - If collection exists, appends new company data instead of skipping.
    """

    client = vector_store.client
    existing_collections = client.list_collections()

    # --- STEP 1: Attach company metadata to each node ---
    for node in nodes:
        node.metadata = node.metadata or {}
        node.metadata["company_name"] = company_name.lower()

    # --- STEP 2: If collection exists, check stats ---
    if collection_name in existing_collections:
        print(f"[INFO] Collection '{collection_name}' found in Milvus. Checking data status...")

        collection_stats = client.get_collection_stats(collection_name)
        entity_count = int(collection_stats["row_count"])
        print(f"[INFO] Collection '{collection_name}' currently has {entity_count} entities.")

        # Load existing index
        existing_index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embed_model,
        )

        # --- STEP 3: Check if this company's data already exists ---
        try:
            existing_data = vector_store.client.query(
                collection_name=collection_name,
                filter=f'company_name == "{company_name.lower()}"',
                output_fields=["company_name"]
            )

            if len(existing_data) > 0:
                print(f"[INFO] Data for company '{company_name}' already exists. Skipping ingestion.")
                return existing_index

            else:
                print(f"[INFO] Ingesting new data for company '{company_name}' into existing collection.")
                existing_index.insert_nodes(nodes)
                return existing_index

        except Exception as e:
            print(f"[WARN] Could not query existing data. Proceeding to ingest. Reason: {e}")
            existing_index.insert_nodes(nodes)
            return existing_index

    # --- STEP 4: Collection doesn't exist — create it fresh ---
    else:
        print(f"[INFO] Collection '{collection_name}' not found. Creating and ingesting documents...")
        print(f"[INFO] Ingesting {len(nodes)} nodes for company '{company_name}'.")

        return VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            embed_model=embed_model,
            show_progress=True,
        )
