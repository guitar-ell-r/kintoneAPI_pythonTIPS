## kintoneのアプリにレコードを1件登録する
## https://cybozu.dev/ja/kintone/docs/rest-api/records/add-record/
import base64
import urllib.request
import json

DOMAIN = "domain"## kintoneのドメイン
LOGIN = "login"## ログイン名
PASS = "password"## パスワード
appno = 21## 取得したいアプリのアプリNo

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
    "文字列__1行_":{"value":"1件登録"}
}
body_fields.append(temp_body)

## 文字列複数行
temp_body = {
    "文字列__複数行_":{"value":"1行目\n2行目"}
}
body_fields.append(temp_body)

## 数値
temp_body = {
    "数値":{"value":"17"}
}
body_fields.append(temp_body)

## 日時 日本の時刻にするには9時間プラスする
temp_body = {
    "日時":{"value":"2023-02-11T18:08:24+09:00"}
}
body_fields.append(temp_body)

## チェックボックス
temp_body = {
    "チェックボックス":{"value":["sample1", "sample2"]}
}
body_fields.append(temp_body)

## ドロップボックス
temp_body = {
    "ドロップダウン":{"value":"sample1"}
}
body_fields.append(temp_body)

## リンク　web
temp_body = {
    "リンク":{"value":"https://cybozu.co.jp/"}
}
body_fields.append(temp_body)

## テーブル
temp_body = {
    "テーブル":{"value":
            [
                {"value":
                    {"文字列__1行__0":{"value":"1行目"},
                    "数値_0":{"value":1}
                    }
                },
                {"value":
                    {"文字列__1行__0":{"value":"2行目"},
                    "数値_0":{"value":2}
                    }
                }
            ]
            }
}
body_fields.append(temp_body)

## 全てのフィールドを辞書型として結合する
body_field = {}
for item_dict in body_fields:
     body_field = {**body_field, **item_dict}

## record部分のbody　フィールドの内容を辞書型で結合
body_record = {"record":body_field}

## アプリ番号部分のbody
body_app = {
    "app":appno
}

## body全体を辞書型として作成する
body = {**body_app, **body_record}
print(body)


## リクエスト作成
req = urllib.request.Request(
            url=uri, ## url
            data=json.dumps(body).encode(), ## body 
            headers=headers, ## header
            method="POST", ## POST
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

