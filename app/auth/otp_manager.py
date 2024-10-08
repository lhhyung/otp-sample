import pyotp


class OTPManager:
    def __init__(self):
        self.secret = None

    def generate_secret(self):
        self.secret = pyotp.random_base32()
        return self.secret

    def generate_otp(self):
        totp = pyotp.TOTP(self.secret)
        return totp

    def verify_otp(self, submitted_otp: str):
        totp = self.generate_otp()
        return totp.verify(submitted_otp)

    def generate_qr_code_uri(self):
        totp = self.generate_otp()
        return totp.provisioning_uri()
