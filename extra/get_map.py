# Convert 

tone_map = {
'āáǎà':'a',
'ēéěè':'e',
'īíǐì':'i',
'ōóǒò':'o',
'ūúǔù':'u',
        }

vowel_tone_map = {
        'a':'āáǎà',
        'e':'ēéěè',
        'i':'īíǐì',
        'o':'ōóǒò',
        'u':'ūúǔù',
        }

vowel_tone = {}
for tk in tone_map.keys():
    for idx, tone in enumerate(tk):
        vowel_tone[tone] = tone_map[tk]


def extract_tone(chars):
    for idx, c in enumerate(chars):
        if c in vowel_tone:
            vowel_wo_tone = vowel_tone[c]
            return (vowel_tone_map[vowel_wo_tone].find(c), chars.replace(c, vowel_wo_tone))
    return None, chars


def apply_tone(tone, chars):
    for idx, c in enumerate(chars):
        if c in vowel_tone_map.keys():
            return chars.replace(c, vowel_tone_map[c][tone])
    return chars


mapping = {}
for line in open('mapping_han_taiwan.txt'):
    parts = line.strip().split()
    count = int(len(parts)/2)
    for i in range(count):
        mapping[parts[i*2+1]] = parts[i*2]

with open('../unitaiwan.js', 'w') as fout:
    fout.write('''function getUnihanMap() {
  var data = " \\
''')

    lc = 0
    for line in open('../unihan.js'):
        lc += 1
        if lc >= 3 and lc <= 41212:
            parts = line.split()
            pinyin = parts[1][:-3]
            tone, pinyin_nt = extract_tone(pinyin)
            gpinyin_nt = mapping.get(pinyin_nt, '?' + pinyin_nt + '?')
            if tone is not None: 
                gpinyin = apply_tone(tone, gpinyin_nt)
            fout.write(f' {parts[0]} {gpinyin}\\n\\\n')

    fout.write('''";

      var arr = data.split("\\n");
      var map = {};
      for(var i = 0; i < arr.length; i++) {
        var str = arr[i].toLowerCase();
        str = str.replace(/^[ \\t]+/g, "");
        var hex = str.split(" ")[0];
        var pinyin = str.split(" ")[1];
        map[hex] = pinyin;
      }
      return map;
    }
    ''')

