import bpy # type: ignore
import functools

def debounce(wait_seconds: float):
    """
    Decorator that postpones a function’s execution until after
    wait_seconds have elapsed since the last time it was invoked.
    Uses bpy.app.timers so it’s safe inside Blender.
    """
    def decorator(fn):
        counter_attr = f"_{fn.__name__}_debounce_counter"
        
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            setattr(wrapped, counter_attr, getattr(wrapped, counter_attr, 0) + 1)
            my_version = getattr(wrapped, counter_attr)
            
            def delayed_call():
                if getattr(wrapped, counter_attr) == my_version:
                    fn(*args, **kwargs)
                return None
            
            bpy.app.timers.register(delayed_call, first_interval=wait_seconds)
        
        return wrapped
    return decorator
