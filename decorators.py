import asyncio 
import functools 
import time 
 
def delay(seconds: float): 
    """Ждет N секунд перед выполнением (для async).""" 
    def decorator(fn): 
        @functools.wraps(fn) 
        async def wrapper(*args, **kwargs): 
            await asyncio.sleep(seconds) 
            return await fn(*args, **kwargs) 
        return wrapper 
    return decorator 
 
def retry(tries=3, delay_sec=1.0): 
    def decorator(fn): 
        @functools.wraps(fn) 
        def wrapper(*args, **kwargs): 
            for i in range(tries): 
                try: return fn(*args, **kwargs) 
                except Exception: 
                    if i == tries - 1: raise 
                    time.sleep(delay_sec) 
        return wrapper 
    return decorator 
