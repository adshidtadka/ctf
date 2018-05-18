
# Q2 Easy Cipher

## 問題文
`
EBG KVVV vf n fvzcyr yrggre fhofgvghgvba pvcure gung ercynprf n yrggre jvgu gur yrggre KVVV yrggref nsgre vg va gur nycunorg. EBG KVVV vf na rknzcyr bs gur Pnrfne pvcure, qrirybcrq va napvrag Ebzr. Synt vf SYNTFjmtkOWFNZdjkkNH. Vafreg na haqrefpber vzzrqvngryl nsgre SYNT.
`

見るからにシーザー暗号っぽい。  
一文字ずつずらしていって意味の通る文章になれば正解ということだろう。  
というわけで文字をずらすコードを作成


```python
def rot_i(text,i):
    plane_text = ''
    for ch in text:
        code = ord(ch)
        if code == 32 or code == 44 or code == 46:
            plane_text += ch
            continue
        if code <= 90:
            code += i
            if code > 90:
                code = code - 90 + 64
        else:
            code += i
            if code > 122:
                code = code - 122 + 96

        plane_text += chr(code)

    return plane_text

```

ちなみUnicodeの対応表は以下:

|スペース  |,|. |A-Z  |a-z  |
|-----------|--|--|------|------|
|32 |44|46 |65-90  |97-122 |



#### フラグ取得スクリプト


```python
cipher = ('EBG KVVV vf n fvzcyr yrggre fhofgvghgvba pvcure gung ercynprf n yrggre jvgu gur yrggre KVVV yrggref nsgre vg va gur nycunorg. '
                  'EBG KVVV vf na rknzcyr bs gur Pnrfne pvcure, qrirybcrq va napvrag Ebzr. Synt vf SYNTFjmtkOWFNZdjkkNH. '
                  'Vafreg na haqrefpber vzzrqvngryl nsgre SYNT.')

for i in range(1,1+25):
    decode = rot_i(cipher,i)
    if decode.find('FLAG') != -1:
        print(decode)
        break
```

    ROT XIII is a simple letter substitution cipher that replaces a letter with the letter XIII letters after it in the alphabet. ROT XIII is an example of the Caesar cipher, developed in ancient Rome. Flag is FLAGSwzgxBJSAMqwxxAU. Insert an underscore immediately after FLAG.


ちなみにROT13はpythonに実装されているので一発でデコード可能


```python
import codecs

codecs.decode(cipher, 'rot13')
```




    'ROT XIII is a simple letter substitution cipher that replaces a letter with the letter XIII letters after it in the alphabet. ROT XIII is an example of the Caesar cipher, developed in ancient Rome. Flag is FLAGSwzgxBJSAMqwxxAU. Insert an underscore immediately after FLAG.'
