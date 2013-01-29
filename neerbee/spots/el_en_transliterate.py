# -*- coding: utf-8 -*-
import re
from string import replace
import unicodedata as ud

dipth_rules = { u'αι': u'aι', u'άι': u'ai', u'αϊ': u'ai', u'γγ': u'gg', 
                u'γκ': u'gk', u'γξ': u'gx', u'γχ': u'gch', u'ει': u'ei', u'έι': u'ei',
                u'εϊ': u'ei', u'ντ': u'nt',
                u'οι': u'oi', u'όι': u'oi', u'ου': u'ou', u'υι': u'yi'}

vowels = {u'α', u'ε', u'η', u'ι', u'ο', u'υ', u'ω',
          u'Α', u'Ε', u'Η', u'Ι', u'Ο', u'Υ', u'Ω'}
          
accented_vowels = {u'ά', u'έ', u'ή', u'ί', u'ό', u'ύ', u'ώ',
                   u'Ά', u'Έ', u'Ή', u'Ί', u'Ό', u'Ύ', u'Ώ'}

ypsilon_is_v_rules = {u'β', u'γ', u'δ', u'ζ', u'λ', u'μ', u'ν', u'ρ',
                  u'Β', u'Γ', u'Δ', u'Ζ', u'Λ', u'Μ', u'Ν', u'Ρ'}

ypsilon_is_f_rules = {u'θ', u'κ', u'ξ', u'π', u'σ', u'τ', u'φ', u'χ', u'ψ'}

single_rules = {u'Α': u'A', u'α': u'a', u'ά': u'a', u'Β': u'V', u'β': u'v', u'Γ': u'G', u'γ': u'g', 
                u'Δ': u'D', u'δ': u'd', u'Ε': u'E', u'Έ': u'E', u'ε': u'e', u'έ': u'e', u'Ζ': u'Z', u'ζ': u'z', 
                u'Η': u'I', u'Ή': u'I', u'η': u'i', u'ή': u'i', u'Θ': u'Th', u'θ': u'th', u'Ι': u'I', 
                u'Ί': u'I', u'ι': u'i', u'ί': u'i', u'ϊ': u'i', u'ΐ': u'i', u'Ϊ': u'I', u'Κ': u'K', u'κ': u'k', 
                u'Λ': u'L', u'λ': u'l', u'Μ': u'M',
                u'μ': u'm', u'Ν': u'N', u'ν': u'n', u'Ξ': u'X', u'ξ': u'x', u'Ο': u'O', u'Ό': u'O',
                u'ο': u'o', u'ό': u'o', u'Π': u'P', u'π': u'p', u'Ρ': u'R', u'ρ': u'r', u'Σ': u'S',
                u'σ': u's', u'ς': u's', u'Τ': u'T', u'τ': u't', u'Υ': u'U', u'Ύ': u'Y', u'Y': u'y', u'ϋ': 'y', u'ΰ': 'y', u'Ϋ': u'Y',
                u'υ': u'u', u'Φ': u'F', u'φ': u'f', u'Χ': u'Ch', u'χ': u'ch', u'Ψ': u'Ps', u'ψ': u'ps', u'Ω': u'O', 
                u'Ώ': u'O', u'ω': u'ο', u'ώ': u'o', u';': u'?'}
            
word_stop = {' ', ',', '.', '!', ';'}

latin_letters = {}

def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_latin_chars(unistr):
    return all(is_latin(uchr)
            for uchr in unistr
            if uchr.isalpha())

def transliterate_word(greek_text):
    latin_text = u""
    skip_next = False

    for position, letter in enumerate(greek_text):
        
        if skip_next:
            skip_next = False
            continue

        if letter in accented_vowels and position != len(greek_text)-1:
            next_letter = greek_text[position+1] 
            if next_letter == u'υ' or next_letter == u'Υ':
                latin_text = latin_text + single_rules[letter] + (u'y' if next_letter == u'υ' else u'Y')   
                skip_next = True
                continue

        dipth = greek_text[position:position+2]
        if dipth in dipth_rules:
            latin_text = latin_text + dipth_rules[dipth]
            skip_next = True
        elif letter == u'υ' or letter == u'Υ':      
            if position == len(greek_text)-1 or greek_text[position+1] in word_stop:
                latin_text = latin_text + (u'f' if letter == u'υ' else u'F')
            else:
                next_letter = greek_text[position+1] 
                if next_letter in ypsilon_is_v_rules or next_letter in vowels:
                    latin_text = latin_text + (u'v' if letter == u'υ' else u'V')
                elif next_letter in ypsilon_is_f_rules:
                    greek_text = greek_text.replace(letter, (u'f' if letter == u'υ' else 'F'), 1)
                    latin_text = latin_text + (u'f' if letter == u'υ' else u'F')       
        elif letter == u'μ' or letter == u'Μ':
            if position == 0 and (greek_text[position+1] == u'π' or greek_text[position+1] == u'Π'):
                latin_text += ('b' if letter == u'μ' else u'B')
                skip_next = True
            elif position + 1 != len(greek_text):
                if (greek_text[position+1] == u'π' or greek_text[position+1] == u'Π') and (position+1 == len(greek_text)-1):
                    latin_text += ('b' if letter == u'μ' else u'B')
                    skip_next = True
                elif (greek_text[position+1] == u'π' or greek_text[position+1] == u'Π') and greek_text[position+2] in word_stop:
                    latin_text += ('b' if letter == u'μ' else u'B')
                    skip_next = True
            else:
                latin_text = latin_text + single_rules[letter]
        elif letter in single_rules:
            latin_text = latin_text + single_rules[letter]
        else:
            latin_text += letter    

    return latin_text        

def transliterate_text(greek_text):
    return " ".join([transliterate_word(word) for word in greek_text.split()])