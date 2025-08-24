"""
Quality validation system for refined philosophical texts.
Ensures refinements maintain fidelity while improving readability.
"""

import re
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
import statistics


class QualityValidator:
    """Validates the quality of refined philosophical texts."""
    
    def __init__(self, threshold_config: Optional[Dict] = None):
        """
        Initialize validator with configurable thresholds.
        
        Args:
            threshold_config: Optional dictionary of threshold values
        """
        self.thresholds = {
            'min_similarity': 0.85,  # Minimum similarity to original
            'max_similarity': 0.98,  # Maximum (to ensure some changes were made)
            'min_word_retention': 0.90,  # Minimum word retention rate
            'max_word_change': 1.15,  # Maximum word count change ratio
            'min_sentence_retention': 0.95,  # Minimum sentence structure retention
            'max_grammar_errors': 5,  # Maximum grammar errors per 1000 words
        }
        
        if threshold_config:
            self.thresholds.update(threshold_config)
        
        # Common Portuguese grammar patterns
        self.grammar_patterns = self._initialize_grammar_patterns()
        
        # Philosophical structure markers
        self.structure_markers = self._initialize_structure_markers()
    
    def _initialize_grammar_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize common Portuguese grammar error patterns."""
        return {
            'double_space': re.compile(r'\s{2,}'),
            'missing_space_after_punctuation': re.compile(r'[.,:;!?][^\s\n"]'),
            'incorrect_quote_spacing': re.compile(r'"\s|\s"'),
            'unmatched_quotes': re.compile(r'"[^"]*$|^[^"]*"'),
            'unmatched_parentheses': re.compile(r'\([^)]*$|^[^(]*\)'),
            'sentence_fragment': re.compile(r'^[a-z]|[.!?]\s+[a-z]'),
            'repeated_words': re.compile(r'\b(\w+)\s+\1\b', re.IGNORECASE),
        }
    
    def _initialize_structure_markers(self) -> Dict[str, List[str]]:
        """Initialize philosophical structure markers to preserve."""
        return {
            'argument_markers': [
                'primeiro', 'segundo', 'terceiro',
                'por um lado', 'por outro lado',
                'além disso', 'ademais', 'outrossim',
                'portanto', 'logo', 'assim', 'consequentemente',
                'no entanto', 'porém', 'contudo', 'todavia'
            ],
            'citation_markers': [
                'cf.', 'op. cit.', 'ibid.', 'apud', 'vide',
                'p.', 'pp.', 'vol.', 'ed.', 'cap.'
            ],
            'latin_expressions': [
                'a priori', 'a posteriori', 'ad hominem', 'per se',
                'ipso facto', 'sine qua non', 'mutatis mutandis'
            ],
            'section_markers': [
                'introdução', 'conclusão', 'capítulo', 'seção',
                'parte', 'tópico', 'questão', 'artigo'
            ]
        }
    
    def validate_refinement(self, original: str, refined: str) -> Tuple[bool, Dict[str, any]]:
        """
        Comprehensive validation of refined text against original.
        
        Args:
            original: Original transcribed text
            refined: Refined version of the text
        
        Returns:
            Tuple of (is_valid, validation_report)
        """
        report = {
            'is_valid': True,
            'similarity_score': 0,
            'word_retention': 0,
            'structure_preservation': 0,
            'grammar_improvements': 0,
            'issues': [],
            'warnings': [],
            'improvements': []
        }
        
        # 1. Calculate text similarity
        similarity = self._calculate_similarity(original, refined)
        report['similarity_score'] = similarity
        
        if similarity < self.thresholds['min_similarity']:
            report['is_valid'] = False
            report['issues'].append(f"Text similarity too low: {similarity:.2%} < {self.thresholds['min_similarity']:.2%}")
        elif similarity > self.thresholds['max_similarity']:
            report['warnings'].append(f"Very few changes made: {similarity:.2%} similarity")
        
        # 2. Check word retention
        word_retention = self._check_word_retention(original, refined)
        report['word_retention'] = word_retention
        
        if word_retention < self.thresholds['min_word_retention']:
            report['is_valid'] = False
            report['issues'].append(f"Too many words changed: {(1-word_retention):.1%} modified")
        
        # 3. Validate structure preservation
        structure_score = self._validate_structure_preservation(original, refined)
        report['structure_preservation'] = structure_score
        
        if structure_score < 0.90:
            report['warnings'].append(f"Philosophical structure may be altered: {structure_score:.2%} preserved")
        
        # 4. Check for grammar improvements
        original_errors = self._count_grammar_errors(original)
        refined_errors = self._count_grammar_errors(refined)
        improvement_rate = (original_errors - refined_errors) / max(original_errors, 1)
        report['grammar_improvements'] = improvement_rate
        
        if refined_errors > original_errors:
            report['warnings'].append(f"Grammar errors increased: {refined_errors} vs {original_errors}")
        else:
            report['improvements'].append(f"Grammar errors reduced by {improvement_rate:.1%}")
        
        # 5. Validate philosophical terms
        term_issues = self._validate_philosophical_terms(original, refined)
        if term_issues:
            report['warnings'].extend(term_issues)
        
        # 6. Check for content loss
        content_loss = self._check_content_loss(original, refined)
        if content_loss:
            report['issues'].extend(content_loss)
            report['is_valid'] = False
        
        # 7. Validate citations and references
        citation_issues = self._validate_citations(original, refined)
        if citation_issues:
            report['warnings'].extend(citation_issues)
        
        return report['is_valid'], report
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _check_word_retention(self, original: str, refined: str) -> float:
        """Check what percentage of original words are retained."""
        original_words = set(original.lower().split())
        refined_words = set(refined.lower().split())
        
        if not original_words:
            return 1.0
        
        retained = original_words.intersection(refined_words)
        return len(retained) / len(original_words)
    
    def _validate_structure_preservation(self, original: str, refined: str) -> float:
        """Validate that philosophical argument structure is preserved."""
        scores = []
        
        # Check preservation of argument markers
        for marker_type, markers in self.structure_markers.items():
            original_markers = sum(1 for m in markers if m in original.lower())
            refined_markers = sum(1 for m in markers if m in refined.lower())
            
            if original_markers > 0:
                preservation_rate = min(refined_markers / original_markers, 1.0)
                scores.append(preservation_rate)
        
        # Check paragraph structure
        original_paragraphs = len([p for p in original.split('\n\n') if p.strip()])
        refined_paragraphs = len([p for p in refined.split('\n\n') if p.strip()])
        
        if original_paragraphs > 0:
            paragraph_preservation = min(refined_paragraphs / original_paragraphs, 1.0)
            scores.append(paragraph_preservation)
        
        return statistics.mean(scores) if scores else 1.0
    
    def _count_grammar_errors(self, text: str) -> int:
        """Count potential grammar errors in text."""
        error_count = 0
        
        for pattern_name, pattern in self.grammar_patterns.items():
            matches = pattern.findall(text)
            error_count += len(matches)
        
        return error_count
    
    def _validate_philosophical_terms(self, original: str, refined: str) -> List[str]:
        """Validate that philosophical terms are correctly preserved."""
        issues = []
        
        # Extract philosophical terms from original
        important_terms = []
        for markers in self.structure_markers['latin_expressions']:
            if markers in original.lower():
                important_terms.append(markers)
        
        # Check if they're preserved in refined
        for term in important_terms:
            if term not in refined.lower():
                issues.append(f"Philosophical term '{term}' may have been altered or removed")
        
        return issues
    
    def _check_content_loss(self, original: str, refined: str) -> List[str]:
        """Check for significant content loss."""
        issues = []
        
        # Check word count change
        original_words = len(original.split())
        refined_words = len(refined.split())
        word_ratio = refined_words / max(original_words, 1)
        
        if word_ratio < 0.85:
            issues.append(f"Significant content loss: {(1-word_ratio):.1%} reduction in word count")
        elif word_ratio > self.thresholds['max_word_change']:
            issues.append(f"Unexpected content addition: {(word_ratio-1):.1%} increase in word count")
        
        # Check for missing sentences
        original_sentences = [s.strip() for s in re.split(r'[.!?]+', original) if s.strip()]
        refined_sentences = [s.strip() for s in re.split(r'[.!?]+', refined) if s.strip()]
        
        sentence_ratio = len(refined_sentences) / max(len(original_sentences), 1)
        if sentence_ratio < self.thresholds['min_sentence_retention']:
            issues.append(f"Sentence structure significantly altered: {(1-sentence_ratio):.1%} change")
        
        return issues
    
    def _validate_citations(self, original: str, refined: str) -> List[str]:
        """Validate that citations and references are preserved."""
        issues = []
        
        # Extract citation patterns
        citation_pattern = re.compile(r'\([^)]*\d{4}[^)]*\)|\[[^\]]*\d{4}[^\]]*\]')
        
        original_citations = citation_pattern.findall(original)
        refined_citations = citation_pattern.findall(refined)
        
        if len(original_citations) != len(refined_citations):
            issues.append(f"Citation count mismatch: {len(original_citations)} → {len(refined_citations)}")
        
        # Check for altered citations
        for orig_cite in original_citations:
            if orig_cite not in refined:
                # Try to find similar citation
                similar = [r for r in refined_citations if self._calculate_similarity(orig_cite, r) > 0.8]
                if similar:
                    issues.append(f"Citation possibly altered: '{orig_cite}' → '{similar[0]}'")
                else:
                    issues.append(f"Citation missing: '{orig_cite}'")
        
        return issues
    
    def generate_quality_report(self, validation_results: Dict) -> str:
        """Generate a human-readable quality report."""
        report = ["## Quality Validation Report\n"]
        
        # Overall status
        status = "✅ PASSED" if validation_results['is_valid'] else "❌ FAILED"
        report.append(f"**Status**: {status}\n")
        
        # Scores
        report.append("### Scores")
        report.append(f"- Text Similarity: {validation_results['similarity_score']:.1%}")
        report.append(f"- Word Retention: {validation_results['word_retention']:.1%}")
        report.append(f"- Structure Preservation: {validation_results['structure_preservation']:.1%}")
        report.append(f"- Grammar Improvement: {validation_results['grammar_improvements']:.1%}")
        
        # Issues
        if validation_results['issues']:
            report.append("\n### 🚨 Critical Issues")
            for issue in validation_results['issues']:
                report.append(f"- {issue}")
        
        # Warnings
        if validation_results['warnings']:
            report.append("\n### ⚠️ Warnings")
            for warning in validation_results['warnings']:
                report.append(f"- {warning}")
        
        # Improvements
        if validation_results['improvements']:
            report.append("\n### ✨ Improvements")
            for improvement in validation_results['improvements']:
                report.append(f"- {improvement}")
        
        return "\n".join(report)
    
    def suggest_corrections(self, text: str) -> List[Dict[str, str]]:
        """Suggest specific corrections for identified issues."""
        suggestions = []
        
        # Check for double spaces
        if re.search(r'\s{2,}', text):
            suggestions.append({
                'issue': 'Multiple consecutive spaces',
                'suggestion': 'Replace multiple spaces with single space',
                'pattern': r'\s{2,}',
                'replacement': ' '
            })
        
        # Check for missing spaces after punctuation
        if re.search(r'[.,:;!?][^\s\n"]', text):
            suggestions.append({
                'issue': 'Missing space after punctuation',
                'suggestion': 'Add space after punctuation marks',
                'pattern': r'([.,:;!?])([^\s\n"])',
                'replacement': r'\1 \2'
            })
        
        # Check for repeated words
        repeated = re.findall(r'\b(\w+)\s+\1\b', text, re.IGNORECASE)
        if repeated:
            suggestions.append({
                'issue': f'Repeated words found: {", ".join(set(repeated))}',
                'suggestion': 'Remove duplicate words',
                'pattern': r'\b(\w+)\s+\1\b',
                'replacement': r'\1'
            })
        
        return suggestions