import requests
import json


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "auth",
        "params": ["erik45beck", "123qwe456rty"],
        "jsonrpc": "2.0",
        "id": 42,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print '\n\n', response, '\n\n'
    return


if __name__ == "__main__":
    main()
