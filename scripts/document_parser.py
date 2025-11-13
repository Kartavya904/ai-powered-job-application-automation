"""
Document Parser Module
Supports parsing of PDF, DOCX, TXT, MD, and JSON files for profile extraction.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

import fitz  # PyMuPDF
from docx import Document


class DocumentParser:
    """Parse various document formats and extract text content."""
    
    def __init__(self):
        self.supported_formats = {'.pdf', '.docx', '.txt', '.md', '.json'}
    
    def parse(self, file_path: Union[str, Path]) -> Dict[str, any]:
        """
        Parse a document and return structured content.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary with 'content', 'metadata', and 'format' keys
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = file_path.suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        parser_map = {
            '.pdf': self._parse_pdf,
            '.docx': self._parse_docx,
            '.txt': self._parse_txt,
            '.md': self._parse_txt,  # Same as txt
            '.json': self._parse_json,
        }
        
        parser = parser_map[file_ext]
        content = parser(file_path)
        
        return {
            'content': content,
            'metadata': {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'format': file_ext,
            },
            'format': file_ext,
        }
    
    def _parse_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file."""
        text_parts = []
        
        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                text_parts.append(text)
            doc.close()
        except Exception as e:
            raise ValueError(f"Error parsing PDF {file_path}: {e}")
        
        return '\n\n'.join(text_parts)
    
    def _parse_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs]
            return '\n\n'.join(paragraphs)
        except Exception as e:
            raise ValueError(f"Error parsing DOCX {file_path}: {e}")
    
    def _parse_txt(self, file_path: Path) -> str:
        """Extract text from TXT or MD file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Error parsing text file {file_path}: {e}")
    
    def _parse_json(self, file_path: Path) -> str:
        """Extract text from JSON file (flattened)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Flatten JSON to text representation
            if isinstance(data, dict):
                text_parts = []
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        text_parts.append(f"{key}: {json.dumps(value, indent=2)}")
                    else:
                        text_parts.append(f"{key}: {value}")
                return '\n'.join(text_parts)
            elif isinstance(data, list):
                return '\n'.join([json.dumps(item, indent=2) for item in data])
            else:
                return str(data)
        except Exception as e:
            raise ValueError(f"Error parsing JSON {file_path}: {e}")
    
    def parse_directory(self, directory: Union[str, Path]) -> List[Dict[str, any]]:
        """
        Parse all supported documents in a directory.
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of parsed document dictionaries
        """
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"Not a directory: {directory}")
        
        parsed_docs = []
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                try:
                    parsed = self.parse(file_path)
                    parsed_docs.append(parsed)
                except Exception as e:
                    print(f"Warning: Failed to parse {file_path}: {e}")
        
        return parsed_docs
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks for embedding.
        
        Args:
            text: Text to chunk
            chunk_size: Maximum characters per chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for punct in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
                    last_punct = chunk.rfind(punct)
                    if last_punct > chunk_size * 0.7:  # If found in last 30%
                        chunk = chunk[:last_punct + 1]
                        end = start + len(chunk)
                        break
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks


def create_profile_json(parsed_docs: List[Dict[str, any]], output_path: Union[str, Path]) -> None:
    """
    Combine parsed documents into a structured profile.json.
    
    Args:
        parsed_docs: List of parsed document dictionaries
        output_path: Path to save profile.json
    """
    profile = {
        'sections': [],
        'metadata': {
            'total_documents': len(parsed_docs),
            'document_types': [doc['format'] for doc in parsed_docs],
        }
    }
    
    for doc in parsed_docs:
        section = {
            'source': doc['metadata']['file_name'],
            'content': doc['content'],
            'metadata': doc['metadata'],
        }
        profile['sections'].append(section)
    
    output_path = Path(output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    print(f"Profile saved to {output_path}")


if __name__ == "__main__":
    # Example usage
    parser = DocumentParser()
    
    # Parse a single file
    # result = parser.parse("data/resume.pdf")
    # print(result['content'][:500])  # First 500 chars
    
    # Parse all documents in data directory
    # docs = parser.parse_directory("data")
    # create_profile_json(docs, "data/profile.json")

