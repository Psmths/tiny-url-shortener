from tinydb import TinyDB, Query
import configparser
import argparse
import random
import string
import time

def gen_rand_id():
    """
    This method will generate a random ID based on the config parameters.
    """
    #Get the length limit for the shortened ID
    config = configparser.ConfigParser()
    config.read('.config')
    length_limit = config['general']['lengthlimit']
    digits = config['general'].getboolean('digits')

    valid = string.ascii_uppercase

    if (digits):
        valid += string.digits

    return ''.join(random.choices(
        valid,
        k = int(length_limit)))


def add_new_link(url):
    """
    This method will add a new link to the database, returning the shortened
    link.
    This will only store the ID as this allows for future migration to a
    different domain or directory.
    """
    #Get configs
    config = configparser.ConfigParser()
    config.read('.config')
    domain = config['general']['domain']
    db_path = config['general']['dbpath']

    db = TinyDB(db_path)

    #Generate an ID
    uid = gen_rand_id()

    #Create a new entry
    new_entry = {
        'location': url,
        'uid': uid,
        'ts': time.time()
    }

    #Insert entry into db
    db.insert(new_entry)

    shortened_url = 'https://' + domain + "/" + uid
    return shortened_url

def lookup_link(shortened_url):
    """
    This method takes a shortened URL and returns the complete URL for redirect.
    """
    #Get configs
    config = configparser.ConfigParser()
    config.read('.config')
    domain = config['general']['domain']
    db_path = config['general']['dbpath']
    age_limit = int(config['general']['agelimit']) * 3600 #max time in seconds

    #Remove everything but the uid
    strip = 'https://' + domain + '/'
    uid = shortened_url.replace(strip,'')

    db = TinyDB(db_path)
    uid_query = Query()
    results = db.search(uid_query.uid == uid)

    #Error duplicate
    if (len(results)) > 1:
        return

    #Error no record found
    if (len(results)) == 0:
        return

    record = results[0]

    #Check if time expired and remove if so
    if not (age_limit == 0): #Disables age limiting
        if (time.time() - float(record['ts']) > float(age_limit)):
            db.remove(uid_query.uid == uid)
            return

    return results[0]['location']


def main():
    print(lookup_link(add_new_link('t2est.com/asdf')))
    print(lookup_link("*"))

if __name__ == "__main__":
    main()
