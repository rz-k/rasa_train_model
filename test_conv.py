import requests



def request_rasa(text):
    url = "http://127.0.0.1:5005/webhooks/rest/webhook"
    try:
        response = requests.post(
            url,
            timeout=10,
            headers={"Content-Type": "application/json"},
            json={"message": text}
        )
        json_data = response.json()
        print(response.text)
        if json_data:
            return json_data[0]['text']
        return False
    except Exception as e:
        print(e)
        return False


while True:
    inp = input("++++++++ # ")
    if inp == "q":
        break

    print(request_rasa(inp))

