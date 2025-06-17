import logging
import re

from rest_framework import serializers

from .models import Productpage,CartItem,Wishlist

logger= logging.getLogger(__name__)

class ProductPageSerializer(serializers.ModelSerializer):
    
    discounted_price = serializers.SerializerMethodField()
    class Meta:
        model=Productpage
        fields=['id','name','price','quantity','discount','discounted_price']
    
    def validate_name(self,value):
        if re.search(r'\d',value):
            logger.error("Name validation failed: contains numbers in the name")
            raise serializers.ValidationError("Name cannot contain numbers")
        return value
    
    def get_discounted_price(self,obj):
        try:
            discount = obj.discount or 0
            return round(obj.price *(1-discount/100),2)
        except Exception:
            return obj.price
    

class CartIteSerializer(serializers.ModelSerializer):
    product = ProductPageSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Productpage.objects.all(),
        source = 'product',
        write_only=True
    )   
    class Meta:
        model = CartItem
        fields = ['id','product','product_id','quantity']
    

        
class WishlistItemSerializer(serializers.ModelSerializer):
    product  = ProductPageSerializer(read_only=True)
    product_id= serializers.PrimaryKeyRelatedField(
        queryset= Productpage.objects.all(),
        source='product',
        write_only=True)
    
    class Meta:
        model=Wishlist
        fields = ['id','product','product_id']
        
    