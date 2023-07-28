import os
import sys
import json
import logging
import traceback

import model

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PREDICTIONS_STREAM_NAME = os.getenv(
    'PREDICTIONS_STREAM_NAME', 'ride-predictions'
)

# RUN_ID = os.getenv('RUN_ID', 'a4b217a84e3a44ad870271b75331eb6c')
RUN_ID = os.getenv('RUN_ID')

TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

model_service = model.init(
    prediction_stream_name=PREDICTIONS_STREAM_NAME,
    run_id=RUN_ID,
    test_run=TEST_RUN,
)


def lambda_handler(event, context):
    # pylint: disable=unused-argument
    # pylint: disable=broad-exception-caught
    try:
        return model_service.lambda_handler(event)
    except Exception:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(
            exception_type, exception_value, exception_traceback
        )
        err_msg = json.dumps(
            {
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string,
            }
        )
        logger.error(err_msg)
    return None
