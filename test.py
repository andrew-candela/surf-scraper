from surf_data.alexa_entrypoint import lambda_handler

def test_request():
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.40a07d17-8338-4bfc-9711-2df397043757",
            "locale": "en-US",
            "timestamp": "2022-08-14T01:02:38Z",
            "intent": {
                "name": "get_conditions",
                "confirmationStatus": "NONE",
                "slots": {
                    "surf_spot": {
                        "name": "surf_spot",
                        "value": "Linda mar",
                        "resolutions": {
                            "resolutionsPerAuthority": [
                                {
                                    "authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.60d60e51-55fd-409e-a5b6-4e0c2857d337.surf_spots",
                                    "status": {
                                        "code": "ER_SUCCESS_MATCH"
                                    },
                                    "values": [
                                        {
                                            "value": {
                                                "name": "Pacifica State Beach",
                                                "id": "1"
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                        "confirmationStatus": "CONFIRMED",
                        "source": "USER"
                    }
                }
            },
            "dialogState": "COMPLETED"
        }
    }

    print(lambda_handler(request, {}))

test_request()
