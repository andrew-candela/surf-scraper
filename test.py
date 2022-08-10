from surf_data.alexa_entrypoint import lambda_handler

def test_request():
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.ddb2d07b-ede1-4f93-a2ff-b512ffe789ae",
            "locale": "en-US",
            "timestamp": "2022-08-10T05:43:43Z",
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
                        "confirmationStatus": "NONE",
                        "source": "USER"
                    }
                }
            },
            "dialogState": "COMPLETED"
	    }
    }

    print(lambda_handler(request, {}))

test_request()
