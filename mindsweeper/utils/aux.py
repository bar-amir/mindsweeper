import re

def camel_to_snake(name):
    name = ''.join(word.title() for word in name.split('_'))
    return name

def snake_to_camel(name):
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name

if __name__ == '__main__':
    pass