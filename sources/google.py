import json
from collections import namedtuple

import requests
from bs4 import BeautifulSoup


def run_query( query=None, count=100, offset=0 ):
    
    results = []

    while len( results ) < count:

        url = "https://www.google.com/search?q={}&start={}".format(
            query,
            offset
        )

        print( url )

        r = requests.get(
            url
        )

        divs = None
        try:
            soup = BeautifulSoup( r.text, features="lxml" )
            
            # grab all search result divs from page
            divs = soup.find_all( 'div', class_="g" )
        
        except AttributeError:
            print( r.text )
            pass

        if not divs:
            break

        for div in divs:
            try:
                st = div.find( 'span', class_="st" )
                
                # remove date labels from search item descriptions
                #st.find_all( 'span', class_="f" ).replace_with( "" )
                
                results.append(
                    st.text
                )
            
            except AttributeError:
                print( r.text )
                pass
        
        offset += len( results )

    print( "\n".join(results) )

    return results


def get_results_for_stems_and_subject( stems=None, subject=None, count=100 ):
    
    # construct query
    q = ""
    
    if( stems and len(stems) > 0 ):
        q = " | ".join(
            ['("{}")'.format( f ) for f in stems]
        )

    if subject is not None:
        if len(q) > 0:
            q = '({}) AND "{}"'.format(q, subject)
        else:
            q = subject

    print( 'google query: {}'.format(q) )
    
    results = []
    offset = 0

    while len( results ) < count:

        items = run_query( 
            query = q,
            offset = offset
        )

        if len( items ) < 1:
            break

        results.extend( items )
        offset += len(items)

    return results


def get_results_for_subject( stems=None, subject=None ):
    return get_results_for_stems_and_subject(
        stems = stems,
        subject = subject
    )


def get_opening_results( stems=None ):
    return get_results_for_stems_and_subject(
        stems = stems
    )


if __name__ == "__main__":

    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


    get_results_for_subject(
        [
            "algorithms are",
            "algorithms will",
            "AI is",
            "AI will",
            "machine learning is",
            "machine learning will"
        ],
        "love"
    )