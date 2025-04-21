from tcc_my_project.security import get_token
from tcc_my_project.settings import Settings
import jwt


def test_get_token(user):
    
    token=get_token(data={'email':user.email})
    decode_token=jwt.decode(token,Settings().SECRET_KEY,algorithms=[Settings().ALGORITHM])

    assert decode_token['sub'] == user.email
    assert 'exp' in decode_token

