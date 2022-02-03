import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """

    """
    logger.info('Event: %s', event)

    response = {'result': 'hello'}
    return response