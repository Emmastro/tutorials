import os
import sys

from radio_okapi import process_data
from radio_okapi_articles import process_article_data

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
SERVICE_NAME = os.getenv("SERVICE_NAME", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 0)
FAIL_RATE = os.getenv("FAIL_RATE", 0)
EXPLICIT_TASK = int(os.getenv("EXPLICIT_TASK", 0))
TASK_OFFSET = int(os.getenv("TASK_OFFSET", 0))
SKIP_TASKS='' # '0 3 4 6 7 9'


def main(sleep_ms=0, fail_rate=0):
        
    if TASK_INDEX in SKIP_TASKS.split():
        print(f"Skipping Stask {TASK_INDEX}")
        return
    if EXPLICIT_TASK !=0:
        index = EXPLICIT_TASK
    else:
        index = int(TASK_INDEX) + TASK_OFFSET

    print(f"Starting Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT} with index {index}")

    # TODO: review why we can't reasign a global variable within a function without getting the unboud error...
    #if SERVICE_NAME =='radio-okapi':
    process_article_data(index)
    #else:
    #process_data(index)
        
    print(f"Completed Task #{TASK_INDEX}.")

if __name__ == "__main__":

    try:
        main(sleep_ms=SLEEP_MS, fail_rate=FAIL_RATE)
    except Exception as e:

        raise e