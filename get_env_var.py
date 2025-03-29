import os

def get_env_var(var_name: str) -> str:
    try:
        return os.environ[var_name]
    except KeyError:
        print(f"Please set the environment variable {var_name}")
        exit(1)