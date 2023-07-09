from jwt import encode, decode


def create_token(data: dict) -> str:
    token: str = encode(
        payload=data, key="5vG9LOgTl1NP1FVaXjztxoLiHlbBYj5M", algorithm="HS256"
    )
    return token


def validate_token(token: str) -> dict:
    data: dict = decode(
        token, key="5vG9LOgTl1NP1FVaXjztxoLiHlbBYj5M", algorithms=["HS256"]
    )
    return data
