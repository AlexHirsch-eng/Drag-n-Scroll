"""
Translation service using MyMemory Translation API
Free translation API without authentication
"""
import requests
import logging
from typing import Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class TranslationService:
    """Service for translating text using MyMemory API"""

    # MyMemory Translation API (free, no auth required)
    DEFAULT_API_URL = "https://api.mymemory.translated.net/get"

    # Language codes
    LANGUAGES = {
        'zh': 'Chinese',
        'ru': 'Russian',
        'en': 'English',
        'kk': 'Kazakh',
    }

    def __init__(self, api_url: str = None):
        """
        Initialize Translation service

        Args:
            api_url: Translation API URL (optional, uses default if not provided)
        """
        self.api_url = api_url or getattr(settings, 'TRANSLATION_API_URL', self.DEFAULT_API_URL)

    def translate(self, text: str, source: str = 'en', target: str = 'ru') -> Optional[str]:
        """
        Translate text using MyMemory API

        Args:
            text: Text to translate
            source: Source language code (default: 'en', use 'zh' for Chinese)
            target: Target language code (default: 'ru')

        Returns:
            Translated text or None if translation fails
        """
        if not text or not text.strip():
            return None

        # MyMemory doesn't support 'auto' - need explicit source
        # Auto-detect Chinese if source is 'auto'
        if source == 'auto':
            if self.is_chinese(text):
                source = 'zh'
            else:
                source = 'en'  # Default to English

        try:
            # MyMemory API uses GET with query parameters
            lang_pair = f"{source}|{target}"
            response = requests.get(
                self.api_url,
                params={
                    'q': text,
                    'langpair': lang_pair
                },
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            # Check response status
            if result.get('responseStatus') == 200:
                translated_text = result.get('responseData', {}).get('translatedText')

                if translated_text:
                    logger.info(f"Translated text from {source} to {target}: {text[:50]}...")
                    return translated_text

            # Fallback: check if there's a match in translation data
            matches = result.get('matches', [])
            if matches:
                best_match = matches[0] if matches else None
                if best_match and 'translation' in best_match:
                    return best_match['translation']

            logger.error(f"Translation API returned unexpected response: {result}")
            return None

        except requests.RequestException as e:
            logger.error(f"Translation API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during translation: {e}")
            return None

    def translate_to_ru(self, text: str, source: str = 'auto') -> Optional[str]:
        """Translate text to Russian"""
        return self.translate(text, source=source, target='ru')

    def translate_to_en(self, text: str, source: str = 'auto') -> Optional[str]:
        """Translate text to English"""
        return self.translate(text, source=source, target='en')

    def is_chinese(self, text: str) -> bool:
        """
        Check if text contains Chinese characters

        Args:
            text: Text to check

        Returns:
            True if text contains Chinese characters
        """
        if not text:
            return False

        # Check for Chinese character ranges
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        return chinese_chars > 0


# Singleton instance
translation_service = TranslationService()
