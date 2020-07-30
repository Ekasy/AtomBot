import apiai, json
import config


def get_smart_talking(message):
    request = apiai.ApiAI(config.TOKEN_AI).text_request()
    request.lang = 'ru'
    request.session_id = 'AtomMark1_bot'
    request.query = message
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']

    if response:
        return response
    else:
        return 'Я вас не понял!'


# print(get_smart_talking(input()))
