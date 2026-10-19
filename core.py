class AppError(Exception): 
    """Базовая ошибка.""" 
class ValidationError(AppError): pass 
class NotFoundError(AppError): pass 
 
import json 
import os 
 
class Config: 
    @staticmethod 
    def get(key: str, default=None, type_cast=str): 
        val = os.getenv(key, default) 
        if val is None: raise AppError(f"Нет переменной {key}") 
        try: return type_cast(val) 
        except ValueError: raise AppError(f"Ошибка типа {key}") 
 
def parse_json(text: str): 
    try: return json.loads(text) 
    except Exception as e: raise ValidationError(f"Bad JSON: {e}") 
