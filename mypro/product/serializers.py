import logging
import re

from rest_framework import serializers

from .models import Productpage

logger= logging.getLogger(__name__)

class ProductPageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Productpage
        fields=['name','price','quantity']
    
    def validate_name(self,value):
        if re.search(r'\d',value):
            logger.error("Name validation failed: contains numbers in the name")
            raise serializers.ValidationError("Name cannot contain numbers")
        return value
   
        