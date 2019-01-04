import re
import math

from textblob import TextBlob

from sources import bing


default_stems = [
    'algorithms are',
    'algorithms will',
    'machine learning is',
    'machine learning will',
    'AI is',
    'AI will'
]

stem_replacements = {
    'algorithms are' : 'we are',
    'algorithms will' : 'we will',
    'machine learning is' : 'we are',
    'machine learning will' : 'we will',
    'ai is' : 'we are',
    'ai will' : 'we will'
}

replacements = {
    'them' : 'us',
    'our' : 'your'
}


def transform_subject( sentence ):
    for stem in default_stems:
        lc_stem = stem.lower()
        for m in re.finditer( lc_stem, sentence.lower() ):
            sentence = "{}{}{}".format(
                sentence[:m.start()],
                stem_replacements[ lc_stem ],
                sentence[m.end():]
            )
    return sentence


re_clauses = re.compile( r'[,\;:]|\W[\-\–\—\−]\W', re.I )
re_conjoiners = re.compile( r'(\band\b)|(\bor\b)', re.I )

def transform_sentence( sentence, stem ):

    # crop sentence to the stem + everything after
    idx = sentence.lower().find( stem.lower() )
    statement = sentence[ idx: ]

    # in some cases, there will be a full stop in the middle of a 'sentence', so truncate
    idx_end = statement.find(".")
    if idx_end > -1:
        statement = statement[:idx_end]

    # find clauses in statement
    m_clauses = list( re_clauses.finditer(statement) )

    # if we've found a truncated statement...
    if "..." in statement:
        m_first_conjoiner = re_conjoiners.search( statement )
        
        # if we haven't matched any conjoiners or clauses in the statement, bail
        if ( len(m_clauses)<1 ) and (m_first_conjoiner is None):
            return None

        # if we haven't bailed, use the first conjoiner or clause marker as a break point
        idx_break = len( statement )
        if m_clauses:
            idx_break = min( idx_break, m_clauses[0].start() -1 )
        if m_first_conjoiner:
             idx_break = min( idx_break, m_first_conjoiner.start() -1 )

        # chop truncated statement down to first clause
        statement = statement[:idx_break]

    # don't want really short statements
    # (split on a space to count words)
    if len( statement.split(' ') ) < 3:
        return None

    # quotations usually turn out weird
    if re.search( '["“”]', statement ):
        return None

    # as do things with a lot of clauses
    if (m_clauses is not None) and ( len(m_clauses) > 3 ):
        return None

    # if we're here, the statement has passed all checks
    return statement


def transform_description( description, stem ):
    # extract sentences
    blob = TextBlob( description )
    for sentence in blob.sentences:
        if stem in sentence:
            transformed = transform_sentence( "%s" % sentence, stem )
            if transformed:
                transformed = transform_subject( transformed )
            return transformed


def process_results( results, stems ):
    
    statements = []
    
    for result in results:
        desc = result.description
        lc_desc = desc.lower()
        for stem in stems:
            if stem.lower() in lc_desc:
                statement = transform_description( desc, stem )
                if statement is not None:
                    print( statement )
                    statements.append( statement )
    
    return statements


def get_opening_statements():
    bing_results = bing.get_opening_results(
        stems = default_stems
    )
    statements = process_results( bing_results, default_stems )
    return statements


def get_statements_for_subject( subject ):
    bing_results = bing.get_results_for_subject(
        stems = default_stems,
        subject = subject
    )
    statements = process_results( bing_results, default_stems )
    return statements


if __name__ == "__main__":
    #print( get_opening_statements() )
    import sys
    subject = sys.argv[1]
    print( get_statements_for_subject( subject ) )
