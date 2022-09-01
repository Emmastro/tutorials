import itertools
import string
import subprocess
import time
import datetime
from dateutil.rrule import rrule, DAILY
from tqdm import tqdm
import pikepdf
from google.cloud import storage
import math


def bruteforce_date_of_birth(start: datetime.datetime, end: datetime.datetime):

    for dt in rrule(DAILY, dtstart=start, until=end):
        password = dt.strftime("%d%m%Y").encode('ascii')

        try:
            pikepdf.open('encrypted/covid_report.pdf', password=password)
            print("password: ", password)
            return

        except pikepdf._qpdf.PasswordError as e:
            pass


def generate_dictionary_dob(start: datetime.datetime, end: datetime.datetime):

    passwords = ""
    for dt in rrule(DAILY, dtstart=start, until=end):
        passwords += dt.strftime("%d%m%Y") + "\n"

    with open('dictionaries/dob.txt', 'w') as f:
        f.write(passwords)


def generate_dictionary_batches(batch_index: int, n_baches: int, password_length: int):

    chars = string.ascii_letters + string.digits
    possible_password = len(chars)**password_length

    n = math.ceil(possible_password/n_baches)
    start = batch_index * n
    end = (batch_index+1) * n

    passwords = itertools.product(chars, repeat=password_length)
    passwords_batch = itertools.islice(passwords, start, end)

    print(f"Generating dictionary batch {batch_index}...")
    with open("dictionary.txt", 'w') as f:
        for i in tqdm(passwords_batch):
            password = ''.join(i) + '\n'

            f.write(password)

    print("Dictionary batch generated")


def bruteforce_john_the_ripper():

    process = subprocess.Popen(['./hack_pdf.sh'], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("stdout", stdout)
    if b"No password hashes left to crack" in stdout:
        print("Password not found")

    else:
        print("Password found")
        upload_password(stdout)


def upload_password(password):

    client = storage.Client()
    bucket = client.get_bucket('cloudrun-job-bruteforce')
    blob = bucket.blob('password.txt')
    blob.upload_from_string(password)


if __name__ == "__main__":

    start_time = time.time()
    generate_dictionary_batches(0, 1000, 6)

    print(f"Time spent: {time.time() - start_time}")
