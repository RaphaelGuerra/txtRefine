"""
Smart chunking module for philosophical texts.
Provides semantic-aware text splitting that preserves argument structure.
"""

import re
from typing import List, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Download required NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class PhilosophicalChunker:
    """Smart chunker that preserves philosophical argument structure."""
    
    def __init__(self, max_words: int = 800, min_words: int = 400):
        self.max_words = max_words
        self.min_words = min_words
        
        # Philosophical discourse markers
        self.argument_markers = [
            r'\b(portanto|logo|assim|consequentemente|então)\b',
            r'\b(primeiro|segundo|terceiro|quarto|quinto)\b',
            r'\b(por um lado|por outro lado)\b',
            r'\b(em primeiro lugar|em segundo lugar)\b',
            r'\b(além disso|ademais|outrossim)\b',
            r'\b(no entanto|porém|contudo|todavia)\b',
            r'\b(com efeito|de fato|na verdade)\b',
        ]
        
        # Section headers common in philosophical texts
        self.section_markers = [
            r'^#{1,3}\s+',  # Markdown headers
            r'^\d+\.\s+',    # Numbered sections
            r'^[IVX]+\.\s+', # Roman numerals
            r'^Capítulo\s+\d+',
            r'^Seção\s+\d+',
            r'^Parte\s+\d+',
        ]
    
    def find_natural_breaks(self, text: str) -> List[int]:
        """Find natural breaking points in the text."""
        breaks = []
        
        # Find paragraph breaks (double newlines)
        for match in re.finditer(r'\n\n+', text):
            breaks.append(match.start())
        
        # Find section headers
        for pattern in self.section_markers:
            for match in re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE):
                breaks.append(match.start())
        
        # Find major argument transitions
        for pattern in self.argument_markers:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Only consider as break if at sentence start
                sentence_start = text.rfind('.', 0, match.start())
                if sentence_start != -1 and match.start() - sentence_start < 5:
                    breaks.append(sentence_start + 1)
        
        return sorted(set(breaks))
    
    def preserve_context_overlap(self, chunks: List[str], overlap_sentences: int = 2) -> List[str]:
        """Add context overlap between chunks for better coherence."""
        if len(chunks) <= 1:
            return chunks
        
        enhanced_chunks = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                # First chunk: add preview of next
                next_sentences = sent_tokenize(chunks[i + 1])[:overlap_sentences]
                enhanced_chunk = chunk + "\n[Continua: " + " ".join(next_sentences) + "...]"
            elif i == len(chunks) - 1:
                # Last chunk: add recap of previous
                prev_sentences = sent_tokenize(chunks[i - 1])[-overlap_sentences:]
                enhanced_chunk = "[...Continuação: " + " ".join(prev_sentences) + "]\n" + chunk
            else:
                # Middle chunks: add both
                prev_sentences = sent_tokenize(chunks[i - 1])[-overlap_sentences:]
                next_sentences = sent_tokenize(chunks[i + 1])[:overlap_sentences]
                enhanced_chunk = ("[...Continuação: " + " ".join(prev_sentences) + "]\n" +
                                chunk + "\n[Continua: " + " ".join(next_sentences) + "...]")
            
            enhanced_chunks.append(enhanced_chunk)
        
        return enhanced_chunks
    
    def chunk_text(self, text: str, preserve_overlap: bool = True) -> List[str]:
        """
        Split text into semantic chunks preserving philosophical structure.
        """
        # Clean text first
        text = text.strip()
        if not text:
            return []
        
        # Find natural breaking points
        breaks = self.find_natural_breaks(text)
        
        # If no natural breaks or text is short, use simple chunking
        words = text.split()
        if len(words) <= self.max_words:
            return [text]
        
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        # Split by sentences for fine-grained control
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            sentence_words = sentence.split()
            sentence_word_count = len(sentence_words)
            
            # Check if adding this sentence would exceed max
            if current_word_count + sentence_word_count > self.max_words:
                # Save current chunk if it meets minimum
                if current_word_count >= self.min_words:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                    current_word_count = sentence_word_count
                else:
                    # Current chunk too small, add sentence anyway
                    current_chunk.append(sentence)
                    current_word_count += sentence_word_count
            else:
                current_chunk.append(sentence)
                current_word_count += sentence_word_count
            
            # Check for natural break point
            current_position = text.find(sentence) + len(sentence)
            if current_position in breaks and current_word_count >= self.min_words:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_word_count = 0
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Add context overlap if requested
        if preserve_overlap and len(chunks) > 1:
            chunks = self.preserve_context_overlap(chunks)
        
        return chunks
    
    def validate_chunks(self, chunks: List[str]) -> Tuple[bool, List[str]]:
        """Validate that chunks preserve philosophical coherence."""
        issues = []
        
        for i, chunk in enumerate(chunks):
            # Check for incomplete citations
            open_quotes = chunk.count('"') % 2
            if open_quotes != 0:
                issues.append(f"Chunk {i+1}: Unmatched quotes")
            
            # Check for incomplete parentheses
            open_parens = chunk.count('(') - chunk.count(')')
            if open_parens != 0:
                issues.append(f"Chunk {i+1}: Unmatched parentheses")
            
            # Check for Latin phrases split across chunks
            latin_patterns = [
                r'\b(a priori|a posteriori|ad hominem|sine qua non|per se|ipso facto)\b',
                r'\b(modus ponens|modus tollens|reductio ad absurdum)\b',
            ]
            for pattern in latin_patterns:
                if re.search(pattern + r'\s*$', chunk, re.IGNORECASE):
                    issues.append(f"Chunk {i+1}: Latin phrase potentially split")
        
        return len(issues) == 0, issues