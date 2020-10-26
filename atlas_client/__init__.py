__version__ = '0.0.9'

# Set default logging handler to avoid "No handler found" warnings.
import logging
logging.getLogger('atlaspyapi').addHandler(logging.NullHandler())
