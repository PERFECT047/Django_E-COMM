from rest_framework import serializers

from seller.models import Seller
from users.models import CustomUser

class SellerSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Seller
        fields = ['name', 'firstname', 'lastname', 'email', 'phone', 'address', 'longitude', 'latitude', 'password', 'password2']

    def save(self):
        seller = Seller(
            name = self.validated_data['name'],
            firstname = self.validated_data['firstname'],
            lastname = self.validated_data['lastname'],
            email = self.validated_data['email'],
            phone = self.validated_data['phone'],
            address = self.validated_data['address'],
            longitude = self.validated_data['longitude'],
            latitude = self.validated_data['latitude'],
            is_seller = True
        )
        print(seller.name)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            print("***********FUCKING NO***********************")
            raise serializers.ValidationError({'password': "Password Must Match."})
        
        seller.set_password(password)
        seller.save()
        return seller