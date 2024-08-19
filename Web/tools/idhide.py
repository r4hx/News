import base64


def encode_id(id):
    return (
        base64.urlsafe_b64encode(id.to_bytes((id.bit_length() + 7) // 8, "big"))
        .decode()
        .rstrip("=")
    )


def decode_id(encoded_id):
    return int.from_bytes(base64.urlsafe_b64decode(encoded_id + "=="), "big")
