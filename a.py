# import our system libraries
import re
import os

# pip3 install prettytable
from prettytable import PrettyTable

# our filename
_FILE: str = 'mem.raw'

# email and url regex pattern
_EMAIL_PATTERN: bytes = b'[\\w\\.-]+@[\\w\\.-]+\\.\\w+' # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
_URL_PATTERN: bytes = b'\\w+://\\w+\\.\\w+\\.\\w+/?[\\w\\.\\?=#]*' # https://stackoverflow.com/questions/44644501/extract-all-urls-in-a-string-with-python3

# our dictionary for saving the results
_CACHE: dict[str, dict] = {'EMAILS': {}, 'URLS': {}, 'UNKNOWN': {}}

try:

    # open our file as file and read it
    with open(_FILE, 'rb') as file:
        # for line in file:
        while True:
            line: bytes = file.read(65_535)  # read 65,535 bytes (this can be hardcoded)

            # find all emails and urls based on the regex given
            emails: list = re.findall(_EMAIL_PATTERN, line)
            urls: list = re.findall(_URL_PATTERN, line)

            '''
            # experimental way
            for item in [*emails, *urls]:
            
                # skip empty lists
                if not item:
                    break
    
                # check which item our list is in
                where: str = 'EMAILS' if item in emails else 'URLS' if item in urls else 'UNKNOWN'
    
                # we have to clean our item AFTER our check, the items in the list are case-sensitive
                item: str = item.lower().strip().decode('utf-8')
    
                # get the current email count from our list, if there's no entry default to 0
                count: int = _CACHE[where].get(item) or 0
    
                # update our dictionary
                _CACHE[where].update({item: count + 1})
            '''

            # loop through our email list
            for email in emails:

                # skip empty lists
                if not email:
                    break

                # strip and change the email case.
                email: str = email.lower().strip().decode('utf-8')

                # check if the email already exists in our dictionary
                found: int = _CACHE['EMAILS'].get(email) or 0
                _CACHE['EMAILS'].update({email: found + 1})

            # loop through our url list
            for url in urls:

                # skip empty lists
                if not url:
                    break

                # strip and change the email case.
                url: str = url.lower().strip().decode('utf-8')

                # check if the email already exists in our dictionary
                found: int = _CACHE['URLS'].get(url) or 0
                _CACHE['URLS'].update({url: found + 1})

            # break the loop once we reach the end of the file
            if not line:
                break

    # create our tables
    _EMAILS: PrettyTable = PrettyTable(['OCCURS', 'EMAIL'])
    _URLS: PrettyTable = PrettyTable(['OCCURS', 'URL'])

    # align our tables
    _EMAILS.align = _URLS.align = 'l'

    # assign titles to each of our tables for the result file
    _EMAILS.title = 'EMAILS'
    _URLS.title = 'URLS'

    # loop through our cache
    for key, value in _CACHE.items():

        # if our key is emails, add it to the email table
        if key == 'EMAILS':
            # loop through our email and occurrence
            for email, occurrence in value.items():
                # append our items to the cache
                _EMAILS.add_row([occurrence, email])

        # if its url, do the that
        if key == 'URLS':
            # loop through our url and occurrence
            for url, occurrence in value.items():
                # append our items to the cache
                _URLS.add_row([occurrence, url])

    for table in (_EMAILS, _URLS):

        # convert out table to a csv string and sort by occurrences
        resultCsv: None = table.get_csv_string(sortby='OCCURS', reversesort=True)

        # get our table title and a random hex for the filename
        fileName: str = f'{table.title}_{os.urandom(6).hex()}.csv'

        # save our file
        with open(fileName, 'a') as f:
            # split the resultCSV by the newline
            for line in resultCsv.split('\n'):
                # save it to the file
                f.write(f'{line}')

        print(f'Saved to {os.getcwd()}\{fileName}..!')

# catch and print any errors
except Exception as e:
    print(e)
