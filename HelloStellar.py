from flask import Flask, redirect
from flask import render_template, request
from stellar_base.keypair import Keypair
import json

HTTP_SERVER_IP = 'localhost'
HTTP_SERVER_PORT = 5000
http_server = Flask(__name__)


def main():
    print(' --- HelloStellar ---')
    http_server.run(HTTP_SERVER_IP, HTTP_SERVER_PORT)
    myAddress = gen_address()
    print(myAddress)


@http_server.route("/gen_address")  # associate http://HTTP_SERVER_IP:HTTP_SERVER_PORT/gen_address with this function
def gen_address():
    kp = Keypair.random()
    public_key = kp.address().decode()
    private_key = kp.seed().decode()
    return json.dumps({'publickey': public_key, 'private_key': private_key})


if __name__ == "__main__":
    main()
