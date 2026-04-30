'''
    memory = await Mem0Memory.create(
        config = {
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": "all-minilm:33m",
                    "ollama_base_url": "http://localhost:11434",
                }
            },
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": "qwen2.5:7b",
                    "ollama_base_url": "http://localhost:11434"
                }
            },
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "mem0_memories",
                    "path": "database/memory",       
                }
            },
        }
    )
    '''