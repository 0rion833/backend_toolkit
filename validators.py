from .core import ValidationError 
 
def check_int(val, name="value"): 
    if isinstance(val, bool) or not isinstance(val, int): raise ValidationError(f"'{name}' должен быть int") 
    return val 
 
def check_str(val, name="value"): 
    if not isinstance(val, str) or not val.strip(): raise ValidationError(f"'{name}' должен быть str") 
    return val 
