from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
# import pymysql
import uitls
import sys
from  jieba.analyse import extract_tags
import string

# sys.setrecursionlimit(100000)
stock_id = '600009'

app = Flask(__name__)


@app.route("/be")
def get_data():
    data = uitls.get_be_data(str(stock_id))
    return jsonify({"股票名称": data[1],"当前价格": data[3],"成交量": data[6],"涨跌幅": data[32],"流通市值": data[44]})


@app.route("/his", methods=["get", "post"])
def get_history_data():
    msg = uitls.get_history_data(str(stock_id))
    print(msg)
    print(type(msg))
    return jsonify({"日期":msg['日期'],"开盘价":msg['开盘价'],"收盘价":msg['收盘价'],"最低价":msg['最低价'],"最高价":msg['最高价']})
        # jsonify({"日期": msg['日期'][0],"开盘价":msg['开盘价'][0]})


@app.route("/gp", methods=["get", "post"])
def get_guping():
    data = uitls.get_guping(stock_id)
    d = []
    for i in data:
        k = i.rstrip(string.digits)
        v = i[len(k):]
        ks = extract_tags(k)
        # print(v)
        for j in ks:
            if not j.isdigit():
                d.append({'name': j, 'value': v})
    return jsonify({'kws':d})



@app.route("/time", methods=["get", "post"])
def get_time():
    return uitls.get_time()


@app.route("/", methods=["get", "post"])
def input_id():
    return render_template("main.html")


@app.route("/ind", methods=["get", "post"])
def get_id():
    global stock_id
    stock_id = request.values.get("股票代码")
    print(stock_id)
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
