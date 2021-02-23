from tinydb import TinyDB, Query
import configparser
import argparse
import random
import string
import time
import bitarray

def owo_encode(s):
    ba = bitarray.bitarray()
    ba.frombytes(s.encode('utf-8'))
    o = ''
    s = 0
    g = ''
    for b in ba:
      if s == 0:
        g = ('u' if b else 'o')
        s = 1
        continue
      if s == 1:
        o = o + (g.upper() if b else g)
        s = 2
        continue
      if s == 2:
        o = o + ('W' if b else 'w')
        s = 3
        continue
      if s == 3:
        o = o + (g.upper() if b else g)
        s = 0
        continue
    return o

def gen_rand_id():
    """
    This method will generate a random ID based on the config parameters.
    """
    # Get the length limit for the shortened ID
    config = configparser.ConfigParser()
    config.read('.config')
    length_limit = config['general'].getint('lengthlimit')
    digits = config['general'].getboolean('digits')

    valid = string.ascii_uppercase

    if (digits):
        valid += string.digits

    return ''.join(random.choices(
        valid,
        k=length_limit))


def add_new_link(url):
    """
    This method will add a new link to the database, returning the shortened
    link.
    This will only store the ID as this allows for future migration to a
    different domain or directory.
    """
    # Get configs
    config = configparser.ConfigParser()
    config.read('.config')
    domain = config['general']['domain'].rstrip('/')
    db_path = config['general']['dbpath']
    owo = config['general'].getboolean('owo')

    db = TinyDB(db_path)

    # Generate an ID
    uid = (owo_encode(url) if owo else gen_rand_id())


    # Add http to URL if not present
    if "http" not in url:
        url = "http://" + url

    # Create a new entry
    new_entry = {
        'location': url,
        'uid': uid,
        'ts': time.time()
    }

    # Insert entry into db
    db.insert(new_entry)

    shortened_url = 'https://' + domain + "/" + uid
    return shortened_url


def lookup_link(shortened_url):
    """
    This method takes a shortened URL and returns the complete
    URL for redirect.
    """
    # Get configs
    config = configparser.ConfigParser()
    config.read('.config')
    domain = config['general']['domain'].rstrip('/')
    db_path = config['general']['dbpath']
    age_limit = config['general'].getint('agelimit') * 3600
    length_limit = config['general'].getint('lengthlimit')

    # Remove everything but the uid
    strip = 'https://' + domain + '/'
    uid = shortened_url.replace(strip, '')

    # Check if request is too long
    if (len(uid) > length_limit):
        return

    db = TinyDB(db_path)
    uid_query = Query()
    results = db.search(uid_query.uid == uid)

    # Error duplicate
    if (len(results)) > 1:
        return

    # Error no record found
    if (len(results)) == 0:
        return

    record = results[0]

    # Check if time expired and remove if so
    if not (age_limit == 0):  # Disables age limiting
        if (time.time() - float(record['ts']) > float(age_limit)):
            db.remove(uid_query.uid == uid)
            return

    return results[0]['location']


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--request',
                        help='Parse a shortened URL request. Takes <shortlink>',
                        nargs='?')
    parser.add_argument('--create',
                        help='Create a shortened URL. Takes <longlink>', nargs='?')

    args = parser.parse_args()

    if (args.create):
        print(add_new_link(args.create))

    if (args.request):
        print(lookup_link(args.request))

if __name__ == "__main__":
    main()
