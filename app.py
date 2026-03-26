import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# 宿舍所有人的 sendkey 列表
all_sendkeys = [
    "SSCT329571ToxBCJwAFBsnbMYV65AvDOpT0",  # 我要上人大
    "SCT329569TG10JqeHcXrH6mAgvVRMWxMgT",  # NCT啾咪
    "SCT329574T03HUP8jlNvZEaBXeXQft1792",  # 单依纯梦女
    "SCT329572TNeetJEYDhFVUHAqnwbdXr9Uj",  # 黎深老婆
    "SCT329573T7iLG2kJbAKPlUkwAMuc1rdjs",  # 软萌女王酱
    "SCT329534Tkq7SUO6Soz2IH2m9WQUIm4UT"  # 茜茜小大王
]


def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1979LvyWhq!',  # 改成你自己的密码
        database='sleep_db',
        cursorclass=pymysql.cursors.DictCursor
    )


def send_wechat(name, status):
    if status == 1:
        msg = f"✅ {name} 睡觉啦 💤"
    else:
        msg = f"☀️ {name} 起床啦"
    data = {"title": "宿舍哄睡提醒", "desp": msg}

    for sendkey in all_sendkeys:
        url = f"https://sctapi.ftqq.com/{sendkey}.send"
        requests.get(url, params=data)


@app.route('/set_status', methods=['POST'])
def set_status():
    data = request.json
    id = data['id']
    status = data['status']

    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT name FROM persons WHERE id = %s", (id,))
        person = cur.fetchone()
        name = person['name']
        cur.execute("UPDATE persons SET status = %s WHERE id = %s", (status, id))
    db.commit()
    db.close()

    send_wechat(name, status)
    return jsonify({"code": 0, "msg": "success"})


if __name__ == '__main__':
    app.run(debug=True)