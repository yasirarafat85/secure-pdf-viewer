# -*- coding: utf-8 -*-
# Generator for Avro-style Bangla phonetic Keyman keyboard (.kmn)
# Scheme v1 -- documented, iterative. User will review and refine.

HEADER = r"""c  Bangla Phonetic  (Avro-style, type English -> get Bangla)
c  Scheme v1 -- generated. See README for the full mapping table.
c  Build: kmc build source/bangla_phonetic.kmn

store(&NAME)            'Bangla Phonetic'
store(&COPYRIGHT)       '(c) Bangla Keyboard Project'
store(&VERSION)         '10.0'
store(&KEYBOARDVERSION) '1.0'
store(&TARGETS)         'windows macosx linux web mobile'
store(&VISUALKEYBOARD)  'bangla_phonetic.kvks'
store(&LAYOUTFILE)      'bangla_phonetic.keyman-touch-layout'

c ---- single-codepoint consonants (used as context for kar + auto-conjunct) ----
store(cons) 'কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ'

begin Unicode > use(main)

group(main) using keys

c =====================================================================
c  1. OI / OU  diphthong transforms  (must come before the i/u vowels)
c     type  O  then I/U
c =====================================================================
  U+09CB + 'I' > U+09C8      c  ( consonant)ো + I  ->  ৈ   (OI-kar)
  U+0993 + 'I' > U+0990      c  ও + I  ->  ঐ
  U+09CB + 'U' > U+09CC      c  (consonant)ো + U  ->  ৌ   (OU-kar)
  U+0993 + 'U' > U+0994      c  ও + U  ->  ঔ

c =====================================================================
c  2. Contextual digraphs : aspirates (base + h) and nasals
c     these must come before the generic consonant / h rules
c =====================================================================
"""

ASPIRATES = [
    ('ক','খ'), ('গ','ঘ'), ('চ','ছ'), ('জ','ঝ'),
    ('ট','ঠ'), ('ড','ঢ'), ('ত','থ'), ('দ','ধ'),
    ('প','ফ'), ('ব','ভ'), ('স','শ'),
]

NASAL = r"""
  'ন' + 'g' > U+0982        c  n + g  ->  ং   (anusvar, e.g. বাংলা)
  'ন' + 'G' > U+0999        c  n + G  ->  ঙ   (velar nasal)
"""

# vowels: (key, independent, kar)  -- kar empty means inherent (consume)
VOWELS = [
    ('a','আ','া'), ('A','আ','া'),
    ('i','ই','ি'), ('I','ঈ','ী'),
    ('u','উ','ু'), ('U','ঊ','ূ'),
    ('e','এ','ে'),
    ('O','ও','ো'),
    ('E','ঐ','ৈ'),
]

# consonants: (latin_key, bengali)
CONS = [
    ('k','ক'),('K','ক'),('q','ক'),
    ('g','গ'),('G','গ'),
    ('c','চ'),('C','চ'),
    ('j','জ'),('J','জ'),('z','জ'),
    ('T','ট'),
    ('D','ড'),
    ('t','ত'),
    ('d','দ'),
    ('N','ণ'),
    ('n','ন'),
    ('p','প'),
    ('f','ফ'),('F','ফ'),
    ('b','ব'),('B','ব'),
    ('v','ভ'),('V','ভ'),
    ('m','ম'),('M','ম'),
    ('y','য়'),('Y','য'),
    ('r','র'),
    ('R','ড়'),
    ('l','ল'),('L','ল'),
    ('S','ষ'),
    ('s','স'),
    ('h','হ'),
    ('x','ক্ষ'),
]

out = []
out.append(HEADER)

for base, asp in ASPIRATES:
    out.append("  '%s' + 'h' > '%s'      c  %s + h  ->  %s" % (base, asp, base, asp))
out.append("  'ড়' + 'h' > 'ঢ়'")   # R then h -> dhh (two-codepoint, harmless)
out.append(NASAL)

out.append("  'গ' + 'g' > 'জ্ঞ'        c  g+g -> জ্ঞ  (e.g. জ্ঞান = ggan)")
out.append("c  --- ঋ / ৃ-kar  via  rri ---")
out.append("  U+09CD U+09B0 + 'r' > context dk(rri)     c  (cons)্র + r -> pending ঋ")
out.append("  U+09CD U+09B0 dk(rri) + 'i' > U+09C3       c  ...+ i -> ৃ-kar (হৃদয়)")
out.append("  U+09B0 U+09CD U+09B0 + 'i' > U+098B        c  word-initial rri -> ঋ")

out.append("c =====================================================================")
out.append("c  3. 'o' : inherent vowel. consonant+o keeps the consonant; else অ")
out.append("c =====================================================================")
out.append("  any(cons) + 'o' > index(cons,1) dk(inh)   c  consonant + o -> consonant + inherent-vowel marker (breaks conjunct)")
out.append("  + 'o' > 'অ'")
out.append("")

out.append("c =====================================================================")
out.append("c  4. Vowels : after a consonant -> kar sign ; otherwise -> full vowel")
out.append("c =====================================================================")
for key, indep, kar in VOWELS:
    out.append("  any(cons) + '%s' > index(cons,1) '%s'      c  consonant + %s -> %s-kar" % (key, kar, key, indep))
    out.append("  + '%s' > '%s'" % (key, indep))
out.append("")

out.append("c =====================================================================")
out.append("c  5. Consonants : after a consonant -> insert hasant (auto-conjunct)")
out.append("c =====================================================================")
for key, ben in CONS:
    out.append("  any(cons) + '%s' > index(cons,1) U+09CD '%s'" % (key, ben))
    out.append("  + '%s' > '%s'" % (key, ben))
out.append("")

out.append("c =====================================================================")
out.append("c  6. Special signs")
out.append("c =====================================================================")
out.append("  + 'H' > U+0983          c  H  ->  ঃ  (visarga)")
out.append("  + '^' > U+0981          c  ^  ->  ঁ  (chandrabindu)")
out.append("  + [K_BKSLASH] > U+09CD  c  \\  ->  ্  (explicit hasant)")
out.append("  + '|' > U+0964          c  |  ->  ।  (danda / full stop)")
out.append("")

out.append("c =====================================================================")
out.append("c  7. Bengali digits  (auto)")
out.append("c =====================================================================")
_bd = {'0':'০','1':'১','2':'২','3':'৩','4':'৪','5':'৫','6':'৬','7':'৭','8':'৮','9':'৯'}
for k,v in _bd.items():
    out.append("  + '%s' > '%s'" % (k,v))
out.append("")

text = "\n".join(out) + "\n"
import io
with io.open('/home/user/secure-pdf-viewer/bangla-keyboard/bangla_phonetic/source/bangla_phonetic.kmn','w',encoding='utf-8') as f:
    f.write(text)
print("WROTE bangla_phonetic.kmn  (%d lines)" % text.count(chr(10)))
