import sys
import os

def resource_path(relative_path):
    """Build edilmiş exe içinde çalışan dosya yolu çözümü"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
