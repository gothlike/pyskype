import requests
import json


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "send_message",
        "params": ["sayonara-kun", "nyan-nyan, Vik"],
        # "params": ["sprey_x24", "nyan-nyan, Alex!"],
        "jsonrpc": "2.0",
        "id": 42,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print '\n\n', response, '\n\n'
    return


if __name__ == "__main__":
    main()
