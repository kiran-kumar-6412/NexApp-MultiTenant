import yaml
import os

def load_queries():
    try:
        yaml_path = os.path.join(os.path.dirname(__file__), "../resources/queries.yaml")
        print(f"Loading YAML from: {yaml_path}")

        with open(yaml_path,"r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        from src.utils import logger
        logger.logging_error(f"Load queries path {str(e)}")
    
Queries=load_queries()