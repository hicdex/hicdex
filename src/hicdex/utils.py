def clean_null_bytes(string: str) -> str:
    return ''.join(string.split('\x00'))


def fromhex(hexbytes: str) -> str:
    string = ''
    try:
        string = bytes.fromhex(hexbytes).decode()
    except Exception:
        try:
            string = bytes.fromhex(hexbytes).decode('latin-1')
        except Exception:
            pass
    return clean_null_bytes(string)
