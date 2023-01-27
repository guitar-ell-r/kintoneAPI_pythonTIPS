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

