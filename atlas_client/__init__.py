__version__ = '0.1.9'

# Set default logging handler to avoid "No handler found" warnings.
import logging
logging.getLogger('atlaspyapi').addHandler(logging.NullHandler())
