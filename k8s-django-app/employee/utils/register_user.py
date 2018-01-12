from django.contrib.auth.models import User

def register_user(self):
    # Define user and password to register accoun test
    self.username = 'minhtran123'
    self.password = 'ABC123'
    self.api_key = '1234'

    # Create new user
    self.user = User.objects.create_user(self.username, 'minhtran@example.com', self.password)
