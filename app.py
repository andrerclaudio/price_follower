# Build-in modules
import logging
import time
from datetime import timedelta
from threading import ThreadError, Thread

# Added modules
from pytictoc import TicToc
from bs4 import BeautifulSoup
import requests

# Project modules

# Print in file
# logging.basicConfig(filename='logs.log',
#                     filemode='w',
#                     level=logging.INFO,
#                     format='%(asctime)s | %(process)d | %(name)s | %(levelname)s:  %(message)s',
#                     datefmt='%d/%b/%Y - %H:%M:%S')

# Print in software terminal
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(process)d | %(name)s | %(levelname)s:  %(message)s',
                    datefmt='%d/%b/%Y - %H:%M:%S')

logger = logging.getLogger(__name__)


# specifying user agent, You can use other user agents
# available on the internet
HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157'
                          'Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})


class ElapsedTime(object):
    """
    Measure the elapsed time between Tic and Toc
    """
    def __init__(self):
        self.t = TicToc()
        self.t.tic()

    def elapsed(self):
        _elapsed = self.t.tocvalue()
        d = timedelta(seconds=_elapsed)
        logger.info('< {} >'.format(d))


class ThreadingProcessQueue(object):
    """
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval):
        """
        Constructor
        """
        self.interval = interval

        thread = Thread(target=run, args=(self.interval,), name='Thread_name')
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution


def run(interval):
    """ Method that runs forever """
    while True:
        try:
            time.sleep(interval)

        except ThreadError as e:
            logger.exception('{}'.format(e))

        finally:
            pass


def application():
    """" All application has its initialization from here """
    logger.info('Main application is running!')

    url = 'https://www.amazon.com.br/dp/B002VBV1R2/?coliid=I2FWYFEM75XDPB&colid=2IGPTPK62VKE4&psc=0&ref_=lv_ov_lig_dp_it'

    # Making the HTTP Request
    webpage = requests.get(url, headers=HEADERS)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # retrieving product title
    try:
        # Outer Tag Object
        title = soup.find("span",
                          attrs={"id": 'productTitle'})

        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip().replace(',', '')
        logger.info("product Title = {}".format(title_string))

    except AttributeError as e:
        logger.exception(e, exc_info=False)

    # retrieving price
    try:
        price = soup.find("span", attrs={'id': 'price'}).string.strip().replace(',', '')
        price = price[:-2] + ',' + price[-2:]
        logger.info(("Products price = {}".format(price)))

    except AttributeError as e:
        logger.exception(e, exc_info=False)



