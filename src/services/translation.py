try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None

def translate(text: str, target_lang: str) -> str:
    """Translate text to target language code (e.g., 'en','tr').

    Uses deep_translator if available; otherwise returns the original text.
    """
    if not text:
        return text
    if GoogleTranslator:
        try:
            return GoogleTranslator(source='auto', target=target_lang).translate(text)
        except Exception:
            return text
    return text
