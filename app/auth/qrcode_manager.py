import qrcode


class QRCodeManager:

    @staticmethod
    def generate_qrcode(qr_code_uri):
        qr_code_image = qrcode.make(qr_code_uri)
        return qr_code_image
