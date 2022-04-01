from flask import Flask, jsonify, current_app
import pandas as pd


def run_app():
    app = Flask(__name__)

    @app.route("/")
    def upload_json():
        foodsafetykorea_new_restaurant_information = pd.read_csv(
            'C:/Users/junseok/Downloads/foodsafetykorea_new_restaurant_information.csv'
        )

        app = Flask(__name__)
        app.config['JSON_AS_ASCII'] = False

        with app.app_context():
            print(app.app_context)

        return jsonify(foodsafetykorea_new_restaurant_information.to_dict('records'))
        # return foodsafetykorea_new_information.to_dict('records')

    with app.app_context():
        print(current_app.name)

    app.config['JSON_AS_ASCII'] = False
    app.run()


if __name__ == "__main__":
    run_app()
