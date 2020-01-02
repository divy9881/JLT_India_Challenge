import warnings

warnings.filterwarnings("ignore")

import spacy

nlp = spacy.load("en_core_web_md")


def find_best_match(kvp: dict, got: str):
    similarity, ans = 0, None
    k1 = nlp(got)
    for k in kvp:
        k2 = nlp(k)
        s = k1.similarity(k2)
        if s >= similarity:
            similarity, ans = s, kvp[k]
    return ans
