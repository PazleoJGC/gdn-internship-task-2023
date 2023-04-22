from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from resources.average import AverageRate
from resources.minmax_last import MinMaxLast
from resources.difference_last import DifferenceLast

app = Flask(__name__)
api = Api(app)

api.add_resource(AverageRate, "/average/<string:currency>/<string:date>")
api.add_resource(MinMaxLast, "/minmax/<string:currency>/last/<int:num_days>")
api.add_resource(DifferenceLast, "/difference/<string:currency>/last/<int:num_days>")

swagger_url = "/swagger"
style_path = "/static/swagger.json"
swagger_ui = get_swaggerui_blueprint(
    swagger_url,
    style_path,
    config={
        "app_name": "NBP API+"
    }
)
app.register_blueprint(swagger_ui, url_prefix=swagger_url)

if __name__ == "__main__":
    app.run(debug=True)