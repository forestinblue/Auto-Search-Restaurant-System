from flask import Flask, jsonify, current_app


def run_app(data):
    app = Flask(__name__)

    @app.route("/")
    def upload_json():
        app = Flask(__name__)
        app.config['JSON_AS_ASCII'] = False

        with app.app_context():
            print(app.app_context)

        return jsonify(data)

    with app.app_context():
        print(current_app.name)

    app.config['JSON_AS_ASCII'] = False
    app.run()


if __name__ == "__main__":
    run_app()
