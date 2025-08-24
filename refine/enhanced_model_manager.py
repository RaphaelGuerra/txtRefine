"""
Enhanced model management for philosophical text refinement.
Integrates smart chunking, terminology database, specialized prompts, and quality validation.
"""

import ollama
import time
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

# Import our new modules
from .smart_chunking import PhilosophicalChunker
from .philosophy_terms import PhilosophyTermsDatabase
from .prompt_templates import PromptTemplates, PhilosophyStyle
from .quality_validator import QualityValidator


class EnhancedModelManager:
    """Enhanced model manager with philosophical specialization."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize enhanced model manager.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = {
            'default_model': 'llama3.2:latest',
            'max_retries': 3,
            'retry_delay': 2,
            'content_loss_threshold': 0.7,
            'enable_smart_chunking': True,
            'enable_term_correction': True,
            'enable_quality_validation': True,
            'chunk_overlap': True,
            'max_words_per_chunk': 800,
            'min_words_per_chunk': 400,
        }
        
        if config:
            self.config.update(config)
        
        # Initialize components
        self.chunker = PhilosophicalChunker(
            max_words=self.config['max_words_per_chunk'],
            min_words=self.config['min_words_per_chunk']
        )
        self.terms_db = PhilosophyTermsDatabase()
        self.prompt_templates = PromptTemplates()
        self.validator = QualityValidator()
        
        # Track processing statistics
        self.stats = {
            'total_chunks_processed': 0,
            'total_terms_corrected': 0,
            'validation_failures': 0,
            'processing_time': 0
        }
    
    def process_text(self, 
                    text: str, 
                    model_name: Optional[str] = None,
                    style: Optional[PhilosophyStyle] = None) -> Tuple[str, Dict]:
        """
        Process philosophical text with all enhancements.
        
        Args:
            text: Text to process
            model_name: Model to use (optional, uses default if not specified)
            style: Philosophy style (optional, auto-detected if not specified)
        
        Returns:
            Tuple of (refined_text, processing_report)
        """
        start_time = time.time()
        model = model_name or self.config['default_model']
        report = {
            'chunks_processed': 0,
            'terms_corrected': [],
            'validation_results': [],
            'processing_time': 0,
            'style_detected': None,
            'warnings': [],
            'improvements': []
        }
        
        # Step 1: Pre-process with term corrections
        if self.config['enable_term_correction']:
            text, term_corrections = self.terms_db.find_and_correct_terms(text)
            report['terms_corrected'] = term_corrections
            self.stats['total_terms_corrected'] += len(term_corrections)
            
            if term_corrections:
                report['improvements'].append(
                    f"Pre-corrected {len(term_corrections)} philosophical terms"
                )
        
        # Step 2: Detect style if not provided
        if style is None:
            style = self.prompt_templates.detect_style(text)
            report['style_detected'] = style.value
        
        # Step 3: Smart chunking
        if self.config['enable_smart_chunking']:
            chunks = self.chunker.chunk_text(
                text, 
                preserve_overlap=self.config['chunk_overlap']
            )
            
            # Validate chunks
            valid, issues = self.chunker.validate_chunks(chunks)
            if not valid:
                report['warnings'].extend(issues)
        else:
            # Fall back to simple chunking
            chunks = self._simple_chunk(text)
        
        report['chunks_processed'] = len(chunks)
        
        # Step 4: Process each chunk
        refined_chunks = []
        for i, chunk in enumerate(chunks, 1):
            refined_chunk = self._refine_chunk_enhanced(
                chunk, model, style, i, len(chunks)
            )
            
            # Validate chunk refinement if enabled
            if self.config['enable_quality_validation']:
                is_valid, validation = self.validator.validate_refinement(
                    chunk, refined_chunk
                )
                
                if not is_valid:
                    report['warnings'].append(
                        f"Chunk {i} failed validation, using fallback"
                    )
                    refined_chunk = self._fallback_refinement(chunk)
                    self.stats['validation_failures'] += 1
                
                report['validation_results'].append(validation)
            
            refined_chunks.append(refined_chunk)
            self.stats['total_chunks_processed'] += 1
        
        # Step 5: Merge refined chunks
        refined_text = self._merge_chunks_intelligently(refined_chunks)
        
        # Step 6: Post-process for final corrections
        refined_text = self._post_process(refined_text)
        
        # Step 7: Final validation
        if self.config['enable_quality_validation']:
            final_valid, final_validation = self.validator.validate_refinement(
                text, refined_text
            )
            report['final_validation'] = final_validation
            
            if not final_valid:
                report['warnings'].append(
                    "Final validation failed - review output carefully"
                )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        report['processing_time'] = processing_time
        self.stats['processing_time'] += processing_time
        
        return refined_text, report
    
    def _refine_chunk_enhanced(self,
                              chunk: str,
                              model_name: str,
                              style: PhilosophyStyle,
                              chunk_num: int,
                              total_chunks: int) -> str:
        """
        Refine a chunk with enhanced prompt templates.
        
        Args:
            chunk: Text chunk to refine
            model_name: Model to use
            style: Philosophy style
            chunk_num: Current chunk number
            total_chunks: Total number of chunks
        
        Returns:
            Refined chunk text
        """
        # Detect context needs
        context_additions = self.prompt_templates.detect_context_needs(chunk)
        
        # Get appropriate prompt
        prompt = self.prompt_templates.get_prompt(
            style, chunk, chunk_num, total_chunks, context_additions
        )
        
        # Try refinement with retries
        for attempt in range(self.config['max_retries']):
            try:
                response = ollama.generate(
                    model=model_name,
                    prompt=prompt,
                    stream=False
                )
                
                refined_text = response['response'].strip()
                
                # Check for content loss
                if len(refined_text) < len(chunk) * self.config['content_loss_threshold']:
                    if attempt < self.config['max_retries'] - 1:
                        time.sleep(self.config['retry_delay'])
                        continue
                    else:
                        return chunk  # Return original on failure
                
                return refined_text
                
            except Exception as e:
                print(f"Error refining chunk {chunk_num}: {e}")
                if attempt < self.config['max_retries'] - 1:
                    time.sleep(self.config['retry_delay'])
                else:
                    return chunk
        
        return chunk
    
    def _simple_chunk(self, text: str) -> List[str]:
        """Simple fallback chunking method."""
        max_words = self.config['max_words_per_chunk']
        words = text.split()
        
        if len(words) <= max_words:
            return [text]
        
        chunks = []
        for i in range(0, len(words), max_words):
            chunk_words = words[i:i + max_words]
            chunks.append(' '.join(chunk_words))
        
        return chunks
    
    def _merge_chunks_intelligently(self, chunks: List[str]) -> str:
        """
        Intelligently merge chunks, removing overlap markers if present.
        
        Args:
            chunks: List of refined chunks
        
        Returns:
            Merged text
        """
        if not chunks:
            return ""
        
        merged = []
        for i, chunk in enumerate(chunks):
            # Remove overlap markers if present
            chunk = chunk.replace('[Continua:', '')
            chunk = chunk.replace('[...Continuação:', '')
            chunk = chunk.replace('...]', '')
            
            # Clean up extra whitespace
            chunk = ' '.join(chunk.split())
            
            merged.append(chunk)
        
        return ' '.join(merged)
    
    def _fallback_refinement(self, chunk: str) -> str:
        """
        Fallback refinement using only term corrections.
        
        Args:
            chunk: Text chunk
        
        Returns:
            Minimally refined chunk
        """
        # Apply only term corrections
        refined, _ = self.terms_db.find_and_correct_terms(chunk)
        
        # Basic grammar fixes
        refined = refined.replace('  ', ' ')  # Remove double spaces
        refined = refined.strip()
        
        return refined
    
    def _post_process(self, text: str) -> str:
        """
        Post-process refined text for final corrections.
        
        Args:
            text: Refined text
        
        Returns:
            Post-processed text
        """
        # Remove any remaining double spaces
        text = ' '.join(text.split())
        
        # Fix common punctuation issues
        text = text.replace(' ,', ',')
        text = text.replace(' .', '.')
        text = text.replace(' :', ':')
        text = text.replace(' ;', ';')
        text = text.replace(' !', '!')
        text = text.replace(' ?', '?')
        
        # Ensure proper spacing after punctuation
        import re
        text = re.sub(r'([.,:;!?])([^\s])', r'\1 \2', text)
        
        # Fix quote spacing
        text = re.sub(r'"\s+', '"', text)
        text = re.sub(r'\s+"', '"', text)
        
        return text
    
    def get_processing_stats(self) -> Dict:
        """Get processing statistics."""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset processing statistics."""
        self.stats = {
            'total_chunks_processed': 0,
            'total_terms_corrected': 0,
            'validation_failures': 0,
            'processing_time': 0
        }
    
    def generate_processing_report(self, report: Dict) -> str:
        """
        Generate a human-readable processing report.
        
        Args:
            report: Processing report dictionary
        
        Returns:
            Formatted report string
        """
        lines = ["## Processing Report\n"]
        
        # Basic stats
        lines.append(f"**Style Detected**: {report.get('style_detected', 'Unknown')}")
        lines.append(f"**Chunks Processed**: {report['chunks_processed']}")
        lines.append(f"**Processing Time**: {report['processing_time']:.2f} seconds")
        
        # Terms corrected
        if report['terms_corrected']:
            lines.append(f"\n### Terms Corrected ({len(report['terms_corrected'])})")
            for term in report['terms_corrected'][:10]:  # Show first 10
                lines.append(f"- '{term['original']}' → '{term['corrected']}'")
            if len(report['terms_corrected']) > 10:
                lines.append(f"... and {len(report['terms_corrected']) - 10} more")
        
        # Validation summary
        if report.get('validation_results'):
            valid_chunks = sum(1 for v in report['validation_results'] if v['is_valid'])
            lines.append(f"\n### Validation Summary")
            lines.append(f"- Valid chunks: {valid_chunks}/{len(report['validation_results'])}")
        
        # Warnings
        if report['warnings']:
            lines.append("\n### ⚠️ Warnings")
            for warning in report['warnings']:
                lines.append(f"- {warning}")
        
        # Improvements
        if report['improvements']:
            lines.append("\n### ✨ Improvements")
            for improvement in report['improvements']:
                lines.append(f"- {improvement}")
        
        return "\n".join(lines)