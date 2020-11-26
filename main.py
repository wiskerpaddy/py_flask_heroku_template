from flask import Flask, render_template
#import os
app = Flask(__name__)

player = "佐々木"

# メニュー, /, メニューを表示
@app.route("/")
def menu():
    return render_template("menu.html", player = player)

# あるく, /walk, 荒野を歩いていた。
@app.route("/walk")                  #ローカル実行用
#@app.route("/walk",methods=['GET'])
def walk():
    message = player + "は荒野を歩いていた。"
    return render_template("action.html", player = player, message = message)

# たたかう, /attack, モンスターと戦った。
@app.route("/attack")                  #ローカル実行用
#@app.route("/attack",methods=['GET'])
def attack():
    message = player + "はモンスターと戦った。"
    return render_template("action.html", player = player, message = message)

#「Hello Flask」と表示する
@app.route("/say_hello")                  #ローカル実行用
#@app.route("/say_hello",methods=['GET'])
def say_hello():
    message = "Hello Flask"
    return render_template("action.html", player = player, message = message)

# 計算する, /calc, モンスターと計算した。
@app.route("/calc")                  #ローカル実行用
#@app.route("/calc",methods=['GET'])
def calc():
    message = player + "は計算した。"
    return render_template("calc.html", player = player, message = message)

if __name__ == "__main__":
    app.run()                            #ローカル実行用
#    port = int(os.getenv("PORT", 5000))
#   app.run(host="0.0.0.0", port=port)
