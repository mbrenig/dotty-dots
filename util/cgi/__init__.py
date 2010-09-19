#!/usr/bin/env python

'''
Script para unescape de caracteres especiais ISO-8859-1
Autor: Mayron Cachina
Contato: mayroncachina@gmail.com
Site: http://cachina.wordpress.com

Egg mantainer & unescape digits
Autor: Vsevolod Balashov
mail/xmpp: vsevolod@balashov.name
site: http://vsevolod.balashov.name
'''

import htmlentitydefs, re

_char = re.compile(r'&(\w+?);')
_dec  = re.compile(r'&#(\d{2,4});')
_hex  = re.compile(r'&#x(\d{2,4});')

def _char_unescape(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)

def unescape(string):
    """back replace html-safe sequences to special characters
        >>> unescape('&lt; &amp; &gt;')
        '< & >'
        >>> unescape('&#39;')
        "'"
        >>> unescape('&#x27;')
        "'"
    
    full list of sequences: htmlentitydefs.entitydefs
    """
    result = _hex.sub(lambda x: unichr(int(x.group(1), 16)),\
        _dec.sub(lambda x: unichr(int(x.group(1))),\
            _char.sub(_char_unescape, string)))
    if string.__class__ != unicode:
        return result.encode('utf-8')
    else:
        return result

__all__ = ['unescape']