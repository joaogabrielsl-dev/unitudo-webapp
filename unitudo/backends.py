from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # O campo 'username' do formulário de login será o nosso e-mail
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            # Nenhum usuário com este e-mail, então não podemos autenticar
            return None

        # Se o usuário existir, verificamos se a senha está correta
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

