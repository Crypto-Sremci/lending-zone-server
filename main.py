import flask
import requests
import argparse
import send_w3

# Fallback to static pricing
# Value is in USDC, it has 6 0s
fallback = False
stattic_price = {"value": 10000000}
error_price = {"value": -1}

# NFTValuation API
nftval_url = "https://api.nftvaluations.com/production/contracts/{address}/tokens/{id}/valuation"
nftval_headers = {"accept": "application/json"}

app = flask.Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/token-price/<address>/<id>')
def token_price(address, id):
    url = nftval_url.format(address=address, id=id)
    response = requests.get(url, headers=nftval_headers)
    result = {}

    if response.status_code == 200:
        result = response.json()
    else:
        print("Error requsting nftval: " + str(response.text))

        if fallback:
            result = stattic_price
        else:
            result = error_price
    
    send_w3.send_price(address, id, result["value"])

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lending Zone Server')
    parser.add_argument('--fallback', dest='fallback', action='store_true')
    parser.add_argument('--port', dest='port', type=int, default=80)
    args = parser.parse_args()

    fallback = args.fallback

    app.run(debug=True, host='0.0.0.0', port=args.port)
