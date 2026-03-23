from loguru import logger

from .client import request_client_object as connect

__ALL__ = ['connect']

logger.disable('streamlabsio')
