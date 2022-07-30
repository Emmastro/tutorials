
import os
import json
import sys
from bruteforce import bruteforce_john_the_ripper, generate_dictionary_random_password
import time


TASK_INDEX = int(os.getenv("CLOUD_RUN_TASK_INDEX", 0))
TASK_ATTEMPT = int(os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0))

N_BACHES = int(os.getenv("N_BACHES", 1000))
PASSWORD_LENGTH = int(os.getenv("PASSWORD_LENGTH", 6))


def main():
    start = time.time()
    print(f"Starting Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT}...")
    generate_dictionary_random_password(0, N_BACHES, PASSWORD_LENGTH)
    bruteforce_john_the_ripper()

    print(f"Completed Task #{TASK_INDEX}. in {time.time() - start} seconds.")


if __name__ == "__main__":

    try:
        main()
    except Exception as err:
        message = f"Task #{TASK_INDEX}, " \
                  + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)
