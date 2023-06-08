import schedule

from dotenv import load_dotenv
load_dotenv()

from jobs import *


if __name__ == '__main__':
    print('Starting consumer...', flush=True)
    start_consumer()