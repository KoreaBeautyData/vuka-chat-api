class UnicornException(Exception):
    def __init__(self, result_msg: str, result_code: int):
        self.result_msg = result_msg
        self.result_code = result_code
