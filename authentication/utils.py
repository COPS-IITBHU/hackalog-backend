from firebase_admin import auth
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ValidationError

class FirebaseAPI:
    @classmethod
    def verify_id_token(cls, id_token):
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except ValueError:
            raise ValidationError('Invalid Firebase ID Token.', HTTP_422_UNPROCESSABLE_ENTITY)

    @classmethod
    def get_email(cls, jwt):
        email = jwt.get('email', '')
        return email

    @classmethod
    def get_name(cls, jwt):
        name = jwt.get('name', '')
        return name

    @classmethod
    def delete_user_by_uid(cls, uid):
        auth.delete_user(uid) 
        