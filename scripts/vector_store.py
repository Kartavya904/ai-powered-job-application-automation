"""
Vector Store Module
Manages FAISS vector database for semantic search of profile documents.
"""

import json
import os
import pickle
from pathlib import Path
from typing import List, Optional, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    """FAISS-based vector store for semantic search."""
    
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        dimension: int = 384,
        index_type: str = "flat",
        model_dir: Optional[Path] = None,
    ):
        """
        Initialize vector store.
        
        Args:
            embedding_model: Name of sentence transformer model
            dimension: Embedding dimension
            index_type: Type of FAISS index ('flat', 'ivf', 'hnsw')
            model_dir: Directory to save/load models
        """
        self.embedding_model_name = embedding_model
        self.dimension = dimension
        self.index_type = index_type
        self.model_dir = Path(model_dir) if model_dir else Path("models")
        self.model_dir.mkdir(exist_ok=True)
        
        # Load embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedder = SentenceTransformer(embedding_model)
        
        # Initialize FAISS index
        self.index = None
        self.metadata = []  # Store metadata for each vector
        
        # Load existing index if available
        self._load_index()
    
    def _create_index(self) -> faiss.Index:
        """Create a new FAISS index based on index_type."""
        if self.index_type == "flat":
            # Exact search, slower but most accurate
            index = faiss.IndexFlatL2(self.dimension)
        elif self.index_type == "ivf":
            # Inverted file index, faster for large datasets
            # Note: Requires training, so we'll use flat for now
            index = faiss.IndexFlatL2(self.dimension)
        elif self.index_type == "hnsw":
            # Hierarchical Navigable Small World, good balance
            # Note: Requires faiss-gpu or special build
            index = faiss.IndexFlatL2(self.dimension)
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")
        
        return index
    
    def add_documents(self, texts: List[str], metadata: Optional[List[dict]] = None) -> None:
        """
        Add documents to the vector store.
        
        Args:
            texts: List of text chunks to embed
            metadata: Optional list of metadata dicts for each text
        """
        if not texts:
            return
        
        print(f"Embedding {len(texts)} documents...")
        embeddings = self.embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        # Normalize embeddings for better cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create index if it doesn't exist
        if self.index is None:
            self.index = self._create_index()
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        
        # Store metadata
        if metadata:
            self.metadata.extend(metadata)
        else:
            # Create default metadata
            self.metadata.extend([{'text': text[:100]} for text in texts])
        
        print(f"Added {len(texts)} documents. Total vectors: {self.index.ntotal}")
    
    def search(self, query: str, k: int = 5) -> List[Tuple[float, dict]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query text
            k: Number of results to return
            
        Returns:
            List of (score, metadata) tuples, sorted by relevance
        """
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # Embed query
        query_embedding = self.embedder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Convert distances to similarity scores (L2 distance -> similarity)
        # Lower distance = higher similarity
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                # Convert L2 distance to similarity (1 / (1 + distance))
                similarity = 1 / (1 + distance)
                results.append((similarity, self.metadata[idx]))
        
        return results
    
    def save(self, index_path: Optional[Path] = None, metadata_path: Optional[Path] = None) -> None:
        """Save index and metadata to disk."""
        if self.index is None:
            print("No index to save.")
            return
        
        index_path = index_path or self.model_dir / "faiss_index.bin"
        metadata_path = metadata_path or self.model_dir / "faiss_metadata.json"
        
        # Save FAISS index
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        
        print(f"Saved index to {index_path}")
        print(f"Saved metadata to {metadata_path}")
    
    def _load_index(self) -> None:
        """Load existing index and metadata from disk."""
        index_path = self.model_dir / "faiss_index.bin"
        metadata_path = self.model_dir / "faiss_metadata.json"
        
        if index_path.exists() and metadata_path.exists():
            try:
                self.index = faiss.read_index(str(index_path))
                
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                
                print(f"Loaded existing index with {self.index.ntotal} vectors")
            except Exception as e:
                print(f"Warning: Failed to load existing index: {e}")
                self.index = None
                self.metadata = []
    
    def clear(self) -> None:
        """Clear all vectors from the index."""
        self.index = None
        self.metadata = []
        print("Vector store cleared.")


if __name__ == "__main__":
    # Example usage
    store = VectorStore()
    
    # Add some sample documents
    # texts = [
    #     "I am a software engineer with 5 years of experience in Python and machine learning.",
    #     "I have worked on multiple projects involving natural language processing and deep learning.",
    #     "My skills include React, Node.js, and full-stack web development.",
    # ]
    # store.add_documents(texts)
    # store.save()
    
    # Search
    # results = store.search("machine learning projects", k=2)
    # for score, metadata in results:
    #     print(f"Score: {score:.3f}, Metadata: {metadata}")

