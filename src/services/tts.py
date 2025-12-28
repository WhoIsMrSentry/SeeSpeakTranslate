import os

def _try_pyttsx3_speak(text: str):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception:
        return False

def _gtts_save_and_play(text: str, lang: str = 'en'):
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        out_file = 'output.mp3'
        tts.save(out_file)
        if os.name == 'nt':
            os.system(f'start {out_file}')
        else:
            os.system(f'xdg-open {out_file} || open {out_file}')
        return True
    except Exception:
        return False

def speak(text: str, lang: str = 'en') -> bool:
    if not text:
        return False
    if _try_pyttsx3_speak(text):
        return True
    return _gtts_save_and_play(text, lang=lang)
