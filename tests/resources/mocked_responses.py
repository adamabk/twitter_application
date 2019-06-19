from requests.exceptions import HTTPError, RequestException


# stated url to ensure that the test is only for Twitter API
BASE_URL = 'https://api.twitter.com'


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise HTTPError("HTTPError Raised")


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

        return mocked_invalid_post

    else:
        def mocked_failed_post(*args, **kwargs):
            if args[0] == BASE_URL + '/oauth2/token':
                return MockResponse({"token_request": "failed"}, 404)

        return mocked_failed_post
