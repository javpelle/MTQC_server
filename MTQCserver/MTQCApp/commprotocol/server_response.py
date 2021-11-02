SUCCESS = 0
ERROR = -1
ERROR_SERVER = -2
WRONG_JSON = -3
USER_PASS_INCORRECT = -4
USER_ALREADY_EXISTS = -5
AUTHORIZATION_DENIED = -6
USER_NOT_VERIFIED = -7
USER_ALREADY_VERIFIED = -8

server_status_dic = {SUCCESS: "Success", ERROR: "Error", ERROR_SERVER: "Error server",
                     WRONG_JSON: "Unexpected or malformed JSON", USER_PASS_INCORRECT: "User or Pass incorrect",
                     USER_ALREADY_EXISTS: "User already exists", AUTHORIZATION_DENIED: "Authorization denied",
                     USER_NOT_VERIFIED: "User has not been verified", USER_ALREADY_VERIFIED: "User already verified"}


class ServerResponse():

    def __init__(self, status: int = None, data: object = None):
        self.dict = {}
        if status is not None:
            self.set_status(status)
        if data is not None:
            self.dict['data'] = data

    def set_status(self, status: int):
        self.dict['status'] = status
        if (status < SUCCESS):
            self.dict['error_message'] = server_status_dic[status]

    def set_data(self, data: object):
        self.dict['data'] = data

    def get(self) -> dict:
        return self.dict
