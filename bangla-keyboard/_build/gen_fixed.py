# -*- coding: utf-8 -*-
# Parse authentic Probhat bn-probhat.mim -> generate Keyman fixed-layout .kmn
import re, io

mim = io.open('/tmp/probhat.mim', encoding='utf-8').read()

# grab the map/trans block
block = mim[mim.find('(map'):]
pairs = []           # (key_char, out_char)
numpad = []          # (vk, out) for KP digits

for raw in block.splitlines():
    line = raw.split(';',1)[0].rstrip()      # drop comments
    line = line.strip()
    if not line.startswith('('): continue
    # KP digits -> bengali
    m = re.match(r'\(\(KP_(\d)\)\s+"(.+)"\)', line)
    if m:
        numpad.append((m.group(1), m.group(2))); continue
    # skip other special-key entries like (G-..), (C-..), (KP_Decimal) ...
    if re.match(r'\(\([A-Za-z]', line): continue
    # simple:  ("KEY" ?X)  or  ("KEY" "STR")
    m = re.match(r'\("((?:\\.|[^"\\])*)"\s+(.+)\)$', line)
    if not m: continue
    key = m.group(1).replace('\\"','"').replace('\\\\','\\')
    val = m.group(2).strip()
    if val.startswith('?'):
        ch = val[1:]
        if ch.startswith('\\'): ch = ch[1:]
        out = ch[0] if ch else ''
    elif val.startswith('"'):
        out = val.strip('"')
    else:
        continue
    if key=='' or out=='': continue
    pairs.append((key, out))

def ktok(k):
    if k=='\\': return '[K_BKSLASH]'
    if k=='`':  return '[K_BKQUOTE]'
    if k=='"':  return "'\"'"       # match " via single quotes
    if k=="'":  return '"\'"'       # match ' via double quotes
    return "'" + k + "'"

def otok(o):
    if o=='\u200c': return 'U+200C'
    if o=='\u200d': return 'U+200D'
    if o=="'": return 'U+0027'
    if o=='"': return "'\"'"
    return "'" + o + "'"

hdr = r"""c  Bangla Fixed - Probhat layout  (authentic, from m17n-db bn-probhat.mim)
c  Fixed 1:1 layout. Shift gives the upper-register letter/sign.
c  Build: kmc build

store(&NAME)            'Bangla Fixed (Probhat)'
store(&COPYRIGHT)       '(c) Bangla Keyboard Project'
store(&VERSION)         '10.0'
store(&KEYBOARDVERSION) '1.0'
store(&TARGETS)         'windows macosx linux web mobile'
store(&VISUALKEYBOARD)  'bangla_fixed.kvks'
store(&LAYOUTFILE)      'bangla_fixed.keyman-touch-layout'

begin Unicode > use(main)

group(main) using keys

"""

out = [hdr]
out.append("c ---- numpad -> Bengali digits ----")
for vk,o in numpad:
    out.append("  + [K_NP%s] > '%s'" % (vk, o))
out.append("")
out.append("c ---- main Probhat map (unshifted + shifted) ----")
for k,o in pairs:
    out.append("  + %s > %s" % (ktok(k), otok(o)))
out.append("")

io.open('/home/user/secure-pdf-viewer/bangla-keyboard/bangla_fixed/source/bangla_fixed.kmn','w',encoding='utf-8').write("\n".join(out)+"\n")
print("parsed pairs:", len(pairs), " numpad:", len(numpad))
print("sample:", pairs[:6])
