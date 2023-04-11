from uuid import uuid4


def generate_string_uuid_hex(slice: int = 8) -> str:
    return uuid4().hex[:slice].upper()
