"""
Embed Personal Documents Script
Parses personal documents (resume, transcripts, projects) and creates vector embeddings.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.document_parser import DocumentParser, create_profile_json
from scripts.vector_store import VectorStore
from scripts.config_loader import get_config
from scripts.logger_config import setup_logger


def main():
    """Main function to embed personal documents."""
    # Setup
    config = get_config()
    logger = setup_logger(
        level=config.get('logging.level', 'INFO'),
        log_file=config.get('logging.log_file', 'logs/run.log')
    )
    
    logger.info("Starting document embedding process...")
    
    # Get data directory
    data_dir = Path("data")
    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        logger.info("Please create the data directory and add your documents (resume.pdf, etc.)")
        return
    
    # Initialize parser
    parser = DocumentParser()
    
    # Parse all documents in data directory
    logger.info(f"Parsing documents in {data_dir}...")
    parsed_docs = parser.parse_directory(data_dir)
    
    if not parsed_docs:
        logger.warning("No documents found to parse. Please add documents to the data/ directory.")
        return
    
    logger.info(f"Parsed {len(parsed_docs)} documents")
    
    # Create profile.json
    profile_path = data_dir / "profile.json"
    create_profile_json(parsed_docs, profile_path)
    logger.info(f"Created profile.json at {profile_path}")
    
    # Initialize vector store
    ai_config = config.get('ai_settings', {})
    embedding_model = ai_config.get('embedding_model', 'all-MiniLM-L6-v2')
    dimension = ai_config.get('vector_db', {}).get('dimension', 384)
    index_type = ai_config.get('vector_db', {}).get('index_type', 'flat')
    
    logger.info(f"Initializing vector store with model: {embedding_model}")
    vector_store = VectorStore(
        embedding_model=embedding_model,
        dimension=dimension,
        index_type=index_type,
        model_dir=Path("models")
    )
    
    # Chunk and embed documents
    all_chunks = []
    all_metadata = []
    
    for doc in parsed_docs:
        content = doc['content']
        chunks = parser.chunk_text(content, chunk_size=500, overlap=50)
        
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadata.append({
                'source_file': doc['metadata']['file_name'],
                'chunk_index': i,
                'total_chunks': len(chunks),
                'file_format': doc['format'],
                'text_preview': chunk[:100] + '...' if len(chunk) > 100 else chunk,
            })
    
    logger.info(f"Created {len(all_chunks)} text chunks from {len(parsed_docs)} documents")
    
    # Add to vector store
    vector_store.add_documents(all_chunks, all_metadata)
    
    # Save vector store
    vector_store.save()
    logger.info("Vector store saved successfully")
    
    # Test search
    logger.info("Testing vector search...")
    test_queries = [
        "machine learning experience",
        "programming languages",
        "work experience",
    ]
    
    for query in test_queries:
        results = vector_store.search(query, k=3)
        logger.info(f"Query: '{query}'")
        for score, metadata in results:
            logger.info(f"  Score: {score:.3f} - {metadata.get('source_file', 'unknown')}")
    
    logger.info("Document embedding process completed successfully!")


if __name__ == "__main__":
    main()

