import logging

class Logger:
    def __init__(self, log_level=logging.INFO, log_format="%(asctime)s - %(levelname)s - %(message)s", log_file="app.log"):
        self.log_level = log_level
        self.log_format = log_format
        self.log_file = log_file
        self.setup_logger()

    def setup_logger(self):
        """Set up a basic logging configuration."""
        logging.basicConfig(
            level=self.log_level,
            format=self.log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.log_file)
            ]
        )

    def get_logger(self, name):
        """Get a logger instance with the specified name."""
        return logging.getLogger(name)
