from .validators import check_int, check_str 
 
class BaseModel: 
    """Магия: проверяет типы при создании объекта!""" 
    def __init__(self, **kwargs): 
        for key, expected_type in self.__annotations__.items(): 
            if key not in kwargs: 
                raise ValueError(f"Отсутствует поле {key}") 
            val = kwargs[key] 
            if expected_type == int: check_int(val, key) 
            elif expected_type == str: check_str(val, key) 
            setattr(self, key, val) 
 
# Пример использования: 
# class User(BaseModel): 
#     name: str 
#     age: int 
