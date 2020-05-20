import re

def upper_camel_to_snake(name):
    name = ''.join(word.title() for word in name.split('_'))
    return name

def snake_to_upper_camel(name):
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name

def url_to_lower_camel(name):
    name = re.sub(r'-([a-z])', lambda x: x.group(1).upper(), name)
    return name

if __name__ == '__main__':
    pass