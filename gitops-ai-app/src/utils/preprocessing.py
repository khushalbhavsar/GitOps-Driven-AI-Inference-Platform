"""
Text Preprocessing - Application Tier
Utility functions for text cleaning and normalization
"""
import re
import html
import unicodedata
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TextPreprocessor:
    """
    Text preprocessing utility for NLP tasks.
    Handles cleaning, normalization, and tokenization.
    """
    
    def __init__(self, max_length: int = 512, lowercase: bool = False):
        self.max_length = max_length
        self.lowercase = lowercase
        
        # Common patterns
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        self.mention_pattern = re.compile(r'@\w+')
        self.hashtag_pattern = re.compile(r'#\w+')
        self.whitespace_pattern = re.compile(r'\s+')
        self.special_chars_pattern = re.compile(r'[^\w\s.,!?\'"-]')
        
    def preprocess(self, text: str) -> str:
        """
        Main preprocessing pipeline.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned and normalized text
        """
        if not text:
            return ""
        
        # Decode HTML entities
        text = self._decode_html(text)
        
        # Normalize unicode
        text = self._normalize_unicode(text)
        
        # Remove URLs
        text = self._remove_urls(text)
        
        # Remove emails
        text = self._remove_emails(text)
        
        # Handle mentions and hashtags
        text = self._clean_social_media(text)
        
        # Remove special characters
        text = self._clean_special_chars(text)
        
        # Normalize whitespace
        text = self._normalize_whitespace(text)
        
        # Optional lowercase
        if self.lowercase:
            text = text.lower()
        
        # Truncate to max length
        text = self._truncate(text)
        
        return text.strip()
    
    def _decode_html(self, text: str) -> str:
        """Decode HTML entities"""
        return html.unescape(text)
    
    def _normalize_unicode(self, text: str) -> str:
        """Normalize unicode characters"""
        # NFKC normalization - compatibility decomposition + canonical composition
        text = unicodedata.normalize('NFKC', text)
        
        # Remove non-printable characters
        text = ''.join(
            char for char in text 
            if unicodedata.category(char) != 'Cc' or char in '\n\t '
        )
        
        return text
    
    def _remove_urls(self, text: str) -> str:
        """Remove URLs from text"""
        return self.url_pattern.sub(' ', text)
    
    def _remove_emails(self, text: str) -> str:
        """Remove email addresses from text"""
        return self.email_pattern.sub(' ', text)
    
    def _clean_social_media(self, text: str) -> str:
        """Clean social media mentions and hashtags"""
        # Remove @ mentions
        text = self.mention_pattern.sub(' ', text)
        # Remove # but keep the word
        text = text.replace('#', ' ')
        return text
    
    def _clean_special_chars(self, text: str) -> str:
        """Remove special characters while keeping punctuation"""
        return self.special_chars_pattern.sub(' ', text)
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace"""
        return self.whitespace_pattern.sub(' ', text)
    
    def _truncate(self, text: str) -> str:
        """Truncate text to max length (word-aware)"""
        if len(text) <= self.max_length:
            return text
        
        # Truncate at word boundary
        truncated = text[:self.max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > 0:
            return truncated[:last_space]
        
        return truncated
    
    def batch_preprocess(self, texts: list) -> list:
        """Preprocess a batch of texts"""
        return [self.preprocess(text) for text in texts]
    
    def extract_features(self, text: str) -> dict:
        """Extract basic text features for analysis"""
        preprocessed = self.preprocess(text)
        words = preprocessed.split()
        
        return {
            'original_length': len(text),
            'processed_length': len(preprocessed),
            'word_count': len(words),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'has_urls': bool(self.url_pattern.search(text)),
            'has_mentions': bool(self.mention_pattern.search(text)),
            'has_hashtags': bool(self.hashtag_pattern.search(text))
        }
