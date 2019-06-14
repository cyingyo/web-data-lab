import time


class Output(object):
    SUCCESS = 200
    ERROR = 400

    def __init__(self):
        pass

    @classmethod
    def output(cls, data, code, message):
        return {
            'responseTime': time.time(),
            'success': True if code == 200 else False,
            'code': code,
            'data': data,
            'message': message
        }

    @classmethod
    def success(cls, data):
        return cls.output(data, Output.SUCCESS, "success")

    @classmethod
    def error(cls):
        return cls.output(None, Output.ERROR, "error")

