from firebase_admin import auth
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ValidationError

class Profile:
    dept_list = {
        'bce': 'Biochemical Engineering',
        'bme': 'Biomedical Engineering',
        'cer': 'Ceramic Engineering',
        'che': 'Chemical Engineering',
        'chy': 'Chemistry',
        'civ': 'Civil Engineering',
        'cse': 'Computer Science and Engineering',
        'ece': 'Electronics Engineering',
        'eee': 'Electrical Engineering',
        'mat': 'Mathematics and Computing',
        'mec': 'Mechanical Engineering',
        'met': 'Metallurgical Engineering',
        'min': 'Mining Engineering',
        'mst': 'Materials Science and Technology',
        'phe': 'Pharmaceutical Engineering and Technology',
        'phy': 'Physics',
        'hss': 'Humanistic Studies'
    }

    @classmethod
    def get_department_code(cls, email):
        username = email.split('@')[0]
        dept_code = username.split('.')[-1][:3]
        return dept_code

    @classmethod
    def verify_email(cls, email):
        username = email.split('@')[0]
        domain = email.split('@')[1]
        if domain not in ['itbhu.ac.in', 'iitbhu.ac.in']:
            return False
        if '.' not in username:
            return False
        dept_code = cls.get_department_code(email)
        if dept_code not in cls.dept_list:
            return False
        return True

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
    def delete_user_by_uid(cls, uid):
        auth.delete_user(uid) 