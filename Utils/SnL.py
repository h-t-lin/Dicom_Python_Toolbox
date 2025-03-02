import json
import yaml

'''save files'''
def generic_save(file, path:str) -> None:
    if path.endswith('.json'): save_json(file, path)
    elif path.endswith('.yaml'): save_yaml(file, path)
    else: save_(file, path)

def save_(file, path:str) -> None:
    '''e.g. .txt'''
    with open(path,'w') as f:
        f.write(file)

def save_json(file, path:str, indent=4) -> None:
    assert path.endswith('.json')
    with open(path,'w') as f:
        f.write(json.dumps(file, indent=indent))

def save_yaml(file, path:str, sort_keys=False) -> None:
    assert path.endswith('.yaml')
    with open(path,'w') as f:
        yaml.dump(file, f, sort_keys=sort_keys)

'''load files'''
def generic_load(path:str):
    if path.endswith('.json'): return load_json(path)
    elif path.endswith('.yaml'): return load_yaml(path)
    else: raise ValueError("This method can only load json and yaml now.")

def load_json(path:str):
    assert path.endswith('.json')
    with open(path, mode='r') as file:
        file_read = file.read()
    return json.loads(file_read)

def load_yaml(path:str, Loader='S'):
    '''
    ### Loader:  
    * S: SafeLoader (default)
    * B: BaseLoader
    * F: FullLoader
    * U: UnsafeLoader
    '''
    assert path.endswith('.yaml')
    if Loader=='B': loader = yaml.BaseLoader
    elif Loader=='F': loader = yaml.FullLoader
    elif Loader=='U': loader = yaml.UnsafeLoader
    else: loader = yaml.SafeLoader
    with open(path, mode='r') as file:
        file_read = file.read()
    return yaml.load(file_read, Loader=loader)

