import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print("Check direct stdout output")
    print(event)
    logger.info('Test log output')

    if event.get('test_exception_log'):
        try:
            raise Exception("exception")
        except:
            logging.exception("Check exception logging")

    if event.get('raise'):
        raise Exception('Test Exception')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
