import hashlib
import base64

from Cryptodome import Random
from Cryptodome.Cipher import AES
from app.config import SECRET_KEY



class AESCipher:

    def __init__(self):
        # 블록사이즈
        self.BS = 16
        # 암호키 sha256 단방향 암호화
        self.key = hashlib.sha256(SECRET_KEY.encode('utf-8')).digest()
        # 패딩
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-s[-1]]

        self.iv = b"\xf0$b\xdb\xd3\x8e]b\xc7x\x19t\x1d'h\xa5"
        # 초기화 벡터(Initialization Vector)
        # CBC(Cipher-Block Chaining) : 최초 평문 1블럭과 IV를 XOR 연산한 다음 암호화하고,
        #                              다음 평문 1블럭은 앞에서 암호화된 결과 블럭과 XOR 연산하여
        #                              다시 암호화한다. 이 과정을 끝까지 반복하는것이 CBC 모드

    def encrypt(self, raw):
        raw = self.pad(raw).encode('utf-8')
        #iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.unpad(cipher.decrypt(enc))

    def encrypt_str(self, raw):
        return self.encrypt(raw).decode('utf-8')

    def decrypt_str(self, enc):
        if type(enc) == str:
            enc = str.encode(enc)
        return self.decrypt(enc).decode('utf-8')
