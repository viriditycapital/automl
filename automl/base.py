from importlib import import_module
import sklearn


def get_all_functions(top_level, function_list, base):
    for name in top_level:
        try:
            module = import_module(base + '.' + name)
        except:
            pass
        try:
            get_all_functions(module.__all__, function_list, base + '.' + name)
        except:
            for func in dir(module):
                function_list.append((base + '.' + name, func))
    return function_list


def get_regression_functions(function_list):
    regressors_list = []
    for (module, attr) in function_list:
        try:
            func = getattr(import_module(module), attr)
            if sklearn.base.is_regressor(func):
                regressors_list.append(func)
        except:
            pass
    return regressors_list


def get_classification_functions(function_list):
    classifiers_list = []
    for (module, attr) in function_list:
        try:
            func = getattr(import_module(module), attr)
            if sklearn.base.is_classifier(func):
                classifiers_list.append(func)
        except:
            pass
    return classifiers_list


function_list = get_all_functions(sklearn.__all__, [], 'sklearn')
regressor_list = get_regression_functions(function_list)
classifier_list = get_classification_functions(function_list)
print(regressor_list)
print(classifier_list)