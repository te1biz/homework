from functools import wraps

def check_that_arg_is(predicate, error_message):
    def wrapper(function):
        @wraps(function)
        def inner(arg):
            if not predicate(arg):
                raise ValueError(error_message)
            return function(arg)
        return inner
    return wrapper


def predicate_is_int(x):
    return type(x) ==  int


def predicate_is_positive(x):
    return x > 0
@check_that_arg_is(predicate_is_int, "число должно быть положительно")
@check_that_arg_is(predicate_is_int, "Значение должно быть целым числом")
def square(x):
    """ возведенеие числа в квадрат """
    return x * x

if __name__ == '__main__':
    print(square(3))
