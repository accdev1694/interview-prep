import json

def load_interview_config():
    """
    Loads the interview configuration from the config.json file.
    """
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config
