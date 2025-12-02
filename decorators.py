import functools

logged_in = True

def auth_logged_in(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        if logged_in == False:
            return print("Please login to perform this action.")
        else:
            return func(*args, **kwargs)
    return decorator_wrapper

def print_args(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        print(func.__name__)
        for idx, e in enumerate(args):
            print(f'{idx}: {e}')
        return func(*args, **kwargs)
    return decorator_wrapper

@auth_logged_in
@print_args
def sum_num(*args):
    return sum(list(args))

@auth_logged_in
@print_args
def concatenate_str(*args):
    return " ".join(args)

@auth_logged_in
@print_args
def sort_list(*args):
    return sorted(list(args))    



def only_strings(func):
  @functools.wraps(func)
  def decorator_wrapper(*args, **kwargs):
    args = tuple(str(a) for a in args)
    kwargs = {key: str(val) for key, val in kwargs.items()}
    return func(*args, **kwargs)
  return decorator_wrapper


@only_strings
def convert_to_str(**kwargs):
  return ', '.join(kwargs.values()) 


lst = ['one', 'two', 'three', 'four', 'five', 3]
joined_str = convert_to_str(kw1=1, kw2='two', kw3=3, kw4='four')

print(joined_str)
print(type(joined_str))
