from flask import Flask, request, jsonify, make_response

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST", "OPTIONS"])
def receive_data():
    if request.method == "OPTIONS":
        # CORSプリフライトリクエストへの対応
        return _build_cors_preflight_response()
    elif request.method == "POST":
        # JSON形式のデータを受け取る
        print("リクエストを受け取りました")
        data = request.get_json()  # JSONデータを取得
        if data is None:
            # データがJSONではない、またはContent-Typeがapplication/jsonでない場合
            print("リクエストが正しい形式ではありません")
            return jsonify({"message": "リクエストが正しい形式ではありません"}), 400
        print("受け取ったデータ:", data)
        # ここでデータを処理する（例: データベースに保存）
        # ...
        return jsonify({"message": "データを受け取りました"}), 200


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8000)
