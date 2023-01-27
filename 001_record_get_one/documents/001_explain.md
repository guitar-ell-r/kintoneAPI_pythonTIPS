# pythonでkintoneアプリのレコードデータを取得する方法（1レコード）

## 最初に

　kintoneのアプリのデータを自動で一括取得したり、登録したりしたい状況があるかと思います。kintoneではREST APIが用意されており、いろいろなプログラム言語等からデータを簡単に取得したり登録したりすることができます。
　そこで、本記事ではpythonを使ってkintoneのアプリからレコード1件取得する方法をご紹介します。

kintone公式のkintone APIの使い方の説明に従います。  
'https://developer.cybozu.io/hc/ja/articles/202331474#step1'

---

## 環境

* windows11  
* python 3.11.1  

モジュールはすべて標準のものを使います。  

---

## 準備するもの

* kintoneアプリ
* 上記の読み取り権限があるログイン名とパスワード
* アプリのレコードデータ

今回は下記のようなアプリを用意しました。
![kintoneのアプリ絵.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118247/770f6a2f-59ca-13ad-3293-de2753ed1b2f.png)

アプリのフィールドとして

* 文字列（1行）　　文字列__1行_
* 数値 　数値
* 複数選択 　複数選択

を用意しました。それぞれ後ろの文字列はフィールドコードになっています。
1つレコードを追加し、そのレコード番号は1とします。

この画像の表示URLは下記の通りです。
'https://devhswe.cybozu.com/k/20/show#record=1'

この場合、devhsweがドメイン、20がアプリ番号、1がレコード番号になっています。
それぞれ必要な情報ですので、確認してみてください。

---

## pythonとkintoneの通信のイメージ

![通信のイメージ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118247/eae1f5bc-060c-2b33-ea53-5e562c8118ce.png)

　kintoneに送るREST APIに必要な情報を手順に従ってフォーマットを整えてkintoneに送信します。正しいフォーマットで送信されるとkintoneからJSONでデータが返ってきます。

---

## プログラム

```python 001_record_get_one.py
import base64
import urllib.request
import json
```

必要なモジュールをインポートします。
すべてpythonの標準モジュールです。

```python 001_record_get_one.py
DOMAIN = "domain"## ドメイン　自環境のものを入れる
LOGIN = "login"## ログイン名　自環境のものを入れる
PASS = "pass"## パス　自環境のものを入れる
appno = 20## 取得したいアプリのアプリNo
record_no = 1## 取得したいレコードのレコード番号
```

ログイン名とパスワードはそれぞれ、ご自分の環境のものを入力してください。
アプリ番号は20、レコード番号は1となります。

次に、kintoneのREST APIを使うためのuriを設定します。
kintoneの公式にレコード取得（1件）の場合は下記をuriとしてください、と書いてあります。

'https://(サブドメイン名).cybozu.com/k/v1/record.json'
このサブドメイン名の部分がDOMAINに相当するので、uriを下記のように作成します。

```python 001_record_get_one.py
uri = "https://" + DOMAIN + ".cybozu.com/k/v1/record.json"
```

kintoneのREST APIのルールで、ログイン名とパスワードを使った文字列をbase64でエンコードしたものをヘッダに記載して送信する、というものがあります。

'https://developer.cybozu.io/hc/ja/articles/201941754-kintone-REST-API%E3%81%AE%E5%85%B1%E9%80%9A%E4%BB%95%E6%A7%98'

　（パスワード認証の部分）

正確には　（ログイン名）:（パスワード）の文字列をbase64でエンコードしたもの、になります。間にコロンが入っていることに注意してください。
これに従ってAUTHという変数を作成します。

```python 001_record_get_one.py
AUTH = base64.b64encode((LOGIN + ":" + PASS).encode())
```

base64モジュールを使ってエンコードします。

次にリクエストのヘッダを作成します。
下記にkintone公式の説明を引用します。

>(2) パラメータを JSON形式で送信する場合（HTTP リクエストのリクエストボディに JSON データをセットする場合）  
リクエストのヘッダとボディの例  
リクエストヘッダ  
GET /k/v1/record.json HTTP/1.1  
Host: example.cybozu.com:443  
X-Cybozu-Authorization: QWRtaW5pc3RyYXRvcjpjeWJvenU=  
Authorization: Basic QWRtaW5pc3RyYXRvcjpjeWJvenU=  
Content-Type: application/json  
Content-Type に application/json を指定して下さい。  
 指定しない場合は JSON が解釈できないため、実行時エラーとなります。

これをpythonでコーディングすると下記ようになります。  

```python 001_record_get_one.py
headers = {
    "Host":DOMAIN + ".cybozu.com:443",
    "X-Cybozu-Authorization":AUTH,
    "Content-Type": "application/json",
}
```

次にリクエストのボディを作成します。
こちらもkintone公式を引用します。

>ボディ  
{  
    "app": 8,  
    "id": 100  
}  

こちらもpythonでコーディングすると下記のようになります。

```python 001_record_get_one.py
body = {
    "app":appno,
    "id":record_no
}
```

これらの情報からkintoneに送信するリクエストを作成します。

```python 001_record_get_one.py
req = urllib.request.Request(
            url=uri, ## url
            data=json.dumps(body).encode(), ## body 
            headers=headers, ## header
            method="GET", ## GET
            )
```

pythonの標準モジュールurllibを使ってリクエストを作成します。
こちらの記事を参考に作成しました。

'https://qiita.com/hoto17296/items/8fcf55cc6cd823a18217'

リクエスト作成に必要なこれまでの情報、uri、body(data)、headersに加えて、どのような方法で送るのかを設定します。こちらも公式説明に「HTTPメソッド」はGETと書いてあるのでその通りにします。

次にkintoneにこのリクエストを送信します。

```python 001_record_get_one.py
try:
    response = urllib.request.urlopen(req)
except urllib.error.URLError as e:
        if hasattr(e, "reason"):
            res_error = (
                "We failed to reach a server." + "\n" +
                "Reason: " + e.reason + "\n"
            )
            print(res_error)
        elif hasattr(e, 'code'):
            res_error = (
                'The server couldn\'t fulfill the request.' + "\n" +
                'Error code: ', e.code + "\n"
            )
            print(res_error)
else:
    res_dict = json.load(response)
    print(res_dict)
```

tryで囲みましたが、リクエスト送信部分は下記です。

```python 001_record_get_one.py
response = urllib.request.urlopen(req)
```

エラーの補足については下記のサイトをほぼ同じように使わせてもらっています。  
'https://docs.python.org/ja/3/howto/urllib2.html'  
（エラーをラップする　の「その2」）

送信に成功すると結果がres_dictに入ってきます。
jsonで返ってくるので、使いやすいように辞書型に変換して格納します。

実際に返ってきたデータのキャプチャを下記に示します。

![res.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118247/97d17eb3-e725-e430-40d9-ca50509c565b.png)

今回、kintoneアプリ上に用意したフィールドは文字列＿1行、数値、複数選択でしたが、それ以外にも付帯情報として、レコード番号や作成日時等々のデータも同時に取得されます。

プログラム全体は下記になります。
また、githubにもアップロードしてあります。「001_ 001_record_get_one.py」になります。

```python 001_record_get_one.py
## kintoneのアプリからレコードを1件取得する
## https://developer.cybozu.io/hc/ja/articles/202331474#step1
import base64
import urllib.request
import json

DOMAIN = "domain"## ドメイン　自環境のものを入れる
LOGIN = "login"## ログイン名　自環境のものを入れる
PASS = "pass"## パス　自環境のものを入れる
appno = 20## 取得したいアプリのアプリNo
record_no = 1## 取得したいレコードのレコード番号

uri = "https://" + DOMAIN + ".cybozu.com/k/v1/record.json"

## https://developer.cybozu.io/hc/ja/articles/201941754-kintone-REST-API%E3%81%AE%E5%85%B1%E9%80%9A%E4%BB%95%E6%A7%98
## パスワード認証　の部分
## LOGIN と PASSを「：」でつないでbase64でエンコード
AUTH = base64.b64encode((LOGIN + ":" + PASS).encode())

## ヘッダ作成
headers = {
    "Host":DOMAIN + ".cybozu.com:443",
    "X-Cybozu-Authorization":AUTH,
    "Content-Type": "application/json",
}
## body作成
body = {
    "app":appno,
    "id":record_no
}
## リクエスト作成
req = urllib.request.Request(
            url=uri, ## url
            data=json.dumps(body).encode(), ## body 
            headers=headers, ## header
            method="GET", ## GET
            )
## リクエスト送信　結果受け取り
try:
    response = urllib.request.urlopen(req)
except urllib.error.URLError as e:## エラーが生じた場合は補足する
    # https://docs.python.org/ja/3/howto/urllib2.html tryの参考
        if hasattr(e, "reason"):
            res_error = (
                "We failed to reach a server." + "\n" +
                "Reason: " + e.reason + "\n"
            )
            print(res_error)
        elif hasattr(e, 'code'):
            res_error = (
                'The server couldn\'t fulfill the request.' + "\n" +
                'Error code: ', e.code + "\n"
            )
            print(res_error)
else:
    res_dict = json.load(response)
    print(res_dict)
```
