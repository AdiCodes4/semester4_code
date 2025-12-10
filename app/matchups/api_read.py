import logging


def get_api_key(filepath: str) -> str:
    '''Read API Key form a file.'''
    try:
        with open(filepath, 'r') as file:
            api_key=file.read().strip()
        return api_key
    except FileNotFoundError as e:
        logging.error(f'Error opening API keyfile {e}')
        return None