# -*- coding: utf-8 -*-
# Codepoint-accurate simulator (matches Keyman context buffer semantics).
DK='\x00'; RRI='\x01'
H='্'; RA='র'
cons=set('কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ')
asp={'ক':'খ','গ':'ঘ','চ':'ছ','জ':'ঝ','ট':'ঠ','ড':'ঢ','ত':'থ','দ':'ধ','প':'ফ','ব':'ভ','স':'শ'}
vowel={'a':('আ','া'),'A':('আ','া'),'i':('ই','ি'),'I':('ঈ','ী'),'u':('উ','ু'),'U':('ঊ','ূ'),
       'e':('এ','ে'),'O':('ও','ো'),'E':('ঐ','ৈ')}
con={'k':'ক','K':'ক','q':'ক','g':'গ','G':'গ','c':'চ','C':'চ','j':'জ','J':'জ','z':'জ','T':'ট','D':'ড',
     't':'ত','d':'দ','N':'ণ','n':'ন','p':'প','f':'ফ','F':'ফ','b':'ব','B':'ব','v':'ভ','V':'ভ','m':'ম',
     'M':'ম','y':'য়','Y':'য','r':'র','R':'ড়','l':'ল','L':'ল','S':'ষ','s':'স','h':'হ','x':'ক্ষ'}
dig={'0':'০','1':'১','2':'২','3':'৩','4':'৪','5':'৫','6':'৬','7':'৭','8':'৮','9':'৯'}
spec={'H':'ঃ','^':'ঁ','|':'।'}

def typ(s):
    o=[]                                   # list of individual codepoints/sentinels
    push=lambda x: o.extend(list(x))
    def tail(n): return ''.join(o[-n:]) if len(o)>=n else ''
    for ch in s:
        last=o[-1] if o else ''
        if ch=='I' and last=='ো': o[-1]='ৈ'; continue
        if ch=='I' and last=='ও': o[-1]='ঐ'; continue
        if ch=='U' and last=='ো': o[-1]='ৌ'; continue
        if ch=='U' and last=='ও': o[-1]='ঔ'; continue
        if ch=='h' and last in asp: o[-1]=asp[last]; continue
        if ch=='g' and last=='ন': o[-1]='ং'; continue
        if ch=='G' and last=='ন': o[-1]='ঙ'; continue
        if ch=='g' and last=='গ': o[-1:]=list('জ্ঞ'); continue
        if ch=='r' and tail(2)==H+RA: o.append(RRI); continue
        if ch=='i' and tail(3)==H+RA+RRI: del o[-3:]; o.append('ৃ'); continue
        if ch=='i' and tail(3)==RA+H+RA: del o[-3:]; o.append('ঋ'); continue
        if ch=='o':
            if last in cons: o.append(DK); continue
            o.append('অ'); continue
        if ch in vowel:
            ind,kar=vowel[ch]; push(kar if last in cons else ind); continue
        if ch in con:
            if last in cons: o.append(H)
            push(con[ch]); continue
        if ch in dig: o.append(dig[ch]); continue
        if ch in spec: o.append(spec[ch]); continue
        o.append(ch)
    return ''.join(c for c in o if c not in (DK,RRI))

tests=[("ami","আমি"),("shixa","শিক্ষা"),("xoma","ক্ষমা"),("ggan","জ্ঞান"),
 ("biggan","বিজ্ঞান"),("hrridoy","হৃদয়"),("rriSi","ঋষি"),("2026 shal","২০২৬ সাল(shal->শাল)"),
 ("kolokata","কলকাতা"),("projukti","প্রজুক্তি"),("bidyaloy","বিদ্যালয়"),
 ("Bangladesh","বাংলাদেশ"),(" School","(ইংরেজি S->ষ..)"),("prithibi","পৃথিবী via prrithibI")]
for t,e in tests:
    print("%-12s -> %-14s  (%s)"%(t,typ(t),e))
