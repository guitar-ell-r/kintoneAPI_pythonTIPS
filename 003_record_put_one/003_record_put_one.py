## kintoneのアプリのレコードを1件更新する
## https://cybozu.dev/ja/kintone/docs/rest-api/records/add-record/
import base64
import urllib.request
import json

## 自分の環境のものを入力すること
DOMAIN = "domain"## kintoneのドメイン
LOGIN = "login"## ログイン名
PASS = "password"## パスワード

appno = 25## 更新したいアプリのアプリNo
record_no = 1## 更新したいアプリのアプリNo

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

## フィールド部分のbodyのリスト
body_fields = []

## 文字列１行
temp_body = {
    "文字列__1行_":{"value":"更新「後」"}
}
body_fields.append(temp_body)

## 複数選択
temp_body = {
    "複数選択":{"value":[]}## 何も選択しない場合は空のリスト
}
body_fields.append(temp_body)

## 全てのフィールドを辞書型として結合する
body_field = {}
for item_dict in body_fields:
     body_field = {**body_field, **item_dict}

## record部分のbody　フィールドの内容を辞書型で結合
body_record = {"record":body_field}

## アプリ番号、レコード番号部分のbody
body_app_id = {
    "app":appno,
    "id":record_no
}

## body全体を辞書型として作成する
body = {**body_app_id, **body_record}
print(body)

## リクエスト作成
req = urllib.request.Request(
            url=uri, ## url
            data=json.dumps(body).encode(), ## body 
            headers=headers, ## header
            method="PUT", ## PUT
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
