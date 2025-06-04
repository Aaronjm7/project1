from django.core.cache import cache
from django.http import HttpResponseForbidden
import time
from django.shortcuts import render

class BlockIPMiddleware:
    MAX_REQUESTS =4
    WINDOW_SECONDS =60
    BLOCK_DURATION =300
    
    def __init__(self,get_response):
        self.get_response = get_response
        
    def __call__(self,request):
        ip=self.get_ip(request)
        now=time.time()
        
        
        #IP DISABLE CHECK
        block_key= f"block:{ip}"
        if cache.get(block_key):
            return render(request,'blocked.html',status=403)
        
        #Track request time
        req_key= f"reqs:{ip}"
        reqs=cache.get(req_key,[])
        reqs=[ts for ts in reqs if now - ts <self.WINDOW_SECONDS]
        reqs.append(now)
        
        if len(reqs)>self.MAX_REQUESTS:
            cache.set(block_key,True,timeout=self.BLOCK_DURATION)
            cache.delete(req_key)
            return render(request,'blocked.html',status=403)
        
        cache.set(req_key,reqs,timeout=self.WINDOW_SECONDS)
        
        return self.get_response(request)
    
    def get_ip(self,request):
        x_forwarded_for= request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    