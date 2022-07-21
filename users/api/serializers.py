from rest_framework import serializers

from users.models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only':True}}
    
    def save(self):
        customuser = CustomUser(
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
            phone = self.validated_data['phone'],
            is_user = True
        )
        print(customuser.username)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            print("***********FUCKING NO***********************")
            raise serializers.ValidationError({'password': "Password Must Match."})
        
        customuser.set_password(password)
        customuser.save()
        return customuser