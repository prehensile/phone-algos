import requests
import json
from collections import namedtuple


K_QUERY_TYPE_NEWS = "news"
K_QUERY_TYPE_WEB = "web"

K_WEB_URL = "https://api.cognitive.microsoft.com/bing/v7.0/search"
K_NEWS_URL = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"

bing_config = None
with open( "config/bing.json" ) as fp:
    bing_config = json.load( fp )


BingResult = namedtuple( 'BingResult', ['description'] )


def run_query( query=None, query_type=None, count=100, offset=0 ):
    
    headers = {
        "Ocp-Apim-Subscription-Key" : bing_config['key']
    }
    
    print( offset )

    params = {
        "q" : query,
        "count" : count,
        "offset" : offset
        # "textDecorations" : True,
        # "textFormat" : "HTML"
    }

    search_url = K_WEB_URL
    if query_type is not None:
        if query_type == K_QUERY_TYPE_NEWS:
            search_url = K_NEWS_URL

    response = requests.get(
        search_url,
        headers=headers,
        params=params
    )
    response.raise_for_status()
    
    results = response.json()
    return results


def parse_rich_caption( rc ):
    d = None
    if rc['_type'] == 'StructuredValue/SectionData':
        buf = []
        for section in rc['sections']:
            if section['_type'] == 'StructuredValue/SimpleSection':
                buf.append( section['description'] )
        d = '.'.join( buf )
    return d


def parse_results( r ):

    results = []

    # web search result
    if r['_type'] == "SearchResponse":
        for item in r['webPages']['value']:
            
            d = None

            if 'richCaption' in item:
                d = parse_rich_caption(
                    item[ 'richCaption' ]
                )
            
            # if we've failed to parse a rich caption, try the snippet
            if (d is None ) and ('snippet') in item:
                d =  item['snippet']
            # import pprint; pprint.PrettyPrinter().pprint(
            #     item['richCaption']
            # )

            results.append(
                BingResult( description = d )
            )
    
    # news search result
    elif r['_type'] == "News":
        for item in r[ 'value' ]:
            results.append(
                BingResult( description = item['description'] )
            )
    
    return results


def get_results_for_stems_and_subject( query_type=None, stems=None, subject=None, count=100 ):
    
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

    print( 'bing query: {}'.format(q) )
    
    results = []
    offset = 0

    while len( results ) < count:

        r = run_query( 
            query = q,
            query_type = query_type,
            offset = offset
        )

        items = parse_results( r )

        if len( items ) < 1:
            break

        results.extend( items )
        offset += len(items)

    return results


def get_results_for_subject( stems=None, subject=None ):
    return get_results_for_stems_and_subject(
        # query_type = K_QUERY_TYPE_WEB,
        query_type = K_QUERY_TYPE_NEWS,
        stems = stems,
        subject = subject
    )


def get_opening_results( stems=None ):
    return get_results_for_stems_and_subject(
        query_type = K_QUERY_TYPE_NEWS,
        stems = stems
    )
