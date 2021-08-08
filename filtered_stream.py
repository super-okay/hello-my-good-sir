from secret_stuff import (
    BEARER_TOKEN,
    API_KEY,
    API_KEY_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def get_rules():
    """
        displays the current added rules
    """
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json(), indent=4))
    return response.json()

def set_rules():
    """
     sets rules for filtered stream
    """
    my_rule = [
        {"value": "@superokay_ -is:reply -is:retweet", "tag": "somebody mentions me"}
    ]
    payload = {"add": my_rule}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json(), indent=4))


if __name__ == "__main__":
    set_rules = set_rules()
    rules = get_rules()