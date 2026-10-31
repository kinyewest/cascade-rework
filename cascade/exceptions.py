class CascadeException(Exception):
    pass

class HTTPException(CascadeException):
    def __init__(self, response, message):
        self.response = response
        self.status = response.status if hasattr(response, 'status') else None
        self.text = message
        super().__init__(f'HTTP {self.status}: {message}')

class Forbidden(HTTPException):
    pass

class NotFound(HTTPException):
    pass

class CaptchaRequired(HTTPException):
    def __init__(self, response, message, data):
        super().__init__(response, message)
        self.captcha_sitekey = data.get('captcha_sitekey')
        self.captcha_service = data.get('captcha_service')
        self.captcha_rqdata = data.get('captcha_rqdata')
        self.captcha_rqtoken = data.get('captcha_rqtoken')
        self.captcha_session_id = data.get('captcha_session_id')
