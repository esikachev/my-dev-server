class MyDevException(Exception):
    status_code = 400
    message = "An unknown message occured"

    def __init__(self, message=None, status_code=None, payload=None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        super(MyDevException, self).__init__(message, status_code)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


class Duplicate(MyDevException):
    message = "Resource already exist"


class NotFound(MyDevException):
    message = 'Resource does not exist'
    status_code = 404


class LengthRequired(MyDevException):
    message = "Length of data not correct"
    status_code = 411


class BadRequest(MyDevException):
    message = "Request is not correct"
