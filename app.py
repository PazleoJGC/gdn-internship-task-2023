from flask import Flask
from flask_restful import Api

from resources.average import AverageRate
from resources.minmax_range import MinMaxRange
from resources.difference_range import DifferenceRange

app = Flask(__name__)
api = Api(app)

api.add_resource(AverageRate, '/average/<string:currency>/<string:date>')
api.add_resource(MinMaxRange, '/minmax/<string:currency>/last/<int:range>')
api.add_resource(DifferenceRange, '/difference/<string:currency>/last/<int:range>')

if __name__ == "__main__":
    app.run(debug=True)