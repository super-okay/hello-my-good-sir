import requests
import os
import json

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
    print("\n---------- GETTING RULES ----------\n")
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
    print("\n---------- SETTING RULES ----------\n")
    print(json.dumps(response.json(), indent=4))


def delete_all_rules(rules):
    """
        deletes all set rules
    """
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print("\n---------- DELETING ALL RULES ----------\n")
    print(json.dumps(response.json(), indent=4))


def get_stream(set):
    """
        opens filtered stream with specified rules
    """
    print("\n---------- BEGINNING STREAM ----------\n")
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    set_rules = set_rules()
    rules = get_rules()
    get_stream(set_rules)

    ##### DELETES ALL RULES #####
    # rules = get_rules()
    # delete_all_rules(rules)