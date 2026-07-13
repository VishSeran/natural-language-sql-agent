import logging

def get_logger(name:str):
    
    try:
        
        if not name:
            raise ValueError("Logger name mustn't be empty")
        
        logging.basicConfig(
            level=logging.INFO,
            format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        name = name.join("-logger")
        logger = logging.getLogger(name)
        return logger
    
    except ValueError as e:
        print(f"value error: {e}")
        raise
    
    except Exception as e:
        print(f"Error in {name}: {e}")
        raise