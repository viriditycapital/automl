import sklearn
from sklearn.base import is_regressor
from sklearn.base import is_classifier
import importlib
import warnings
import gc
import pandas as pd
warnings.filterwarnings("ignore") #ignore depreciation warnings

top_level = sklearn.__all__
base = 'sklearn.'


def get_all_functions(funclist, totlist, base): # worst code you've ever seen
    for i in funclist:
        try:
            mod = importlib.import_module(base + i)
        except:
            pass
        try:
            temp = mod.__all__
            get_all_functions(temp, totlist, base + i)
        except:
            for func in dir(mod):
                totlist.append((base + i, func))
    return totlist
function_list = get_all_functions(top_level, [], base)


def get_regression_functions(function_list):
    reglist = []
    for (mod, m) in function_list:
        try:
            mod = importlib.import_module(mod)
            func = getattr(mod, m)
            if is_regressor(func):
                reglist.append(func)
        except:
            pass
    return reglist


def get_classification_functions(function_list):
    classlist = []
    for (mod, m) in function_list:
        try:
            mod = importlib.import_module(mod)
            func = getattr(mod, m)
            if is_classifier(func):
                classlist.append(func)
        except:
            pass
    return classlist


# https://stackoverflow.com/questions/492519/timeout-on-a-function-call
import multiprocessing.pool
import functools
def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator


def regressor(x_train, x_test, y_train, y_test):
    print("Starting...\n")
    d = {}
    r = list(set(get_regression_functions(function_list)))
    time = len(r)
    count = 0
    for func in r:
        print(str(func), str(count + 1) + "/" + str(time))
        try:
            score = fit_and_score(func, x_train, x_test, y_train, y_test)
            d[str(func)] = score
        except TimeoutError:
            print("TIMED OUT!")
            time -= 1
            pass
        except:
            time -= 1
            pass
        count+=1
    print("Finished!\n")
    return pd.Series(d, name="Score")


def classifier(x_train, x_test, y_train, y_test):
    print("Starting...\n")
    d = {}
    c = list(set(get_classification_functions(function_list)))
    time = len(c)
    count = 0
    for func in c:
        print(str(func), str(count + 1) + "/" + str(time))
        try:
            score = fit_and_score(func, x_train, x_test, y_train, y_test)
            d[str(func)] = score
        except TimeoutError:
            print("TIMED OUT!")
            time -= 1
            pass
        except:
            time -= 1
            pass
        count += 1
    print("Finished!\n")
    return pd.Series(d, name='Score')


@timeout(30)
def fit_and_score(func, x_train, x_test, y_train, y_test):
    x = func()
    x.fit(x_train, y_train)
    s = x.score(x_test, y_test)
    del(x)
    gc.collect()
    return s