BASE_URL = 'https://api.twitter.com'


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_request_get(success):
    if success:
        def mocked_success_get(*args, **kwargs):
            if args[0] == BASE_URL + '/1.1/statuses/user_timeline.json':
                return MockResponse({"response_status": "succeeded"}, 200)
        return mocked_success_get

    else:
        def mocked_failure_get(*args, **kwargs):
            if args[0] == BASE_URL + '/1.1/statuses/user_timeline.json':
                return MockResponse({"response_status": "failed"}, 404)
        return mocked_failure_get


def mocked_request_post(response_type):
    if response_type == 'success':
        def mocked_success_post(*args, **kwargs):
            if args[0] == BASE_URL + '/oauth2/token':
                return MockResponse({"token_type": "success_token", "access_token": "your_token"}, 200)

        return mocked_success_post

    elif response_type == 'invalid_token':
        # In case the authentication token is not provided
        def mocked_invalid_post(*args, **kwargs):
             if args[0] == BASE_URL + '/oauth2/token':
                return MockResponse({"token_request": "invalid_token"}, 200)

        return mocked_failure_post

    def mocked_failed_post(*args, **kwargs):
        if args[0] == BASE_URL + '/oauth2/token':
            return MockResponse({"token_request": "failed"}, 404)
