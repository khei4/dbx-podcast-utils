from flask import Flask, request, jsonify, make_response

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import html

from google.cloud import texttospeech


def text_to_speech(text: str, outfile: str) -> str:
    """Converts plaintext to SSML and
    generates synthetic audio from SSML

    Args:

    text: text to synthesize
    outfile: filename to use to store synthetic audio

    Returns:
    String of synthesized audio
    """

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'
    escaped_lines = html.escape(text)

    # Convert plaintext to SSML in order to wait two seconds
    #   between each line in synthetic speech
    ssml = "<speak>{}</speak>".format(
        escaped_lines.replace("\n", '\n<break time="2s"/>')
    )

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("FEMALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Selects the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type

    request = texttospeech.SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    response = client.synthesize_speech(request=request)

    # Writes the synthetic audio to the output file.
    with open(outfile, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + outfile)


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
        articleBody = data["body"].replace("\n", " ")[:4080]

        text_to_speech(
            f"""{articleBody}""" + " by Hanchan Panda",
            "output.mp3",
        )
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
