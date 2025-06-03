from django.core.cache import cache

FAILED_ATTEMPTS_PREFIX= "login_fail_"
LOCKOUT_PREFIX="lockout_"
FAILED_LIMIT =3
LOCKOUT_TIME=300

def get_cache_key(username):
    return f"{FAILED_ATTEMPTS_PREFIX}{username.lower()}"

def get_lockout_key(username):
    return f"{LOCKOUT_PREFIX}{username.lower()}"

def is_locked_out(username):
    return cache.get(get_lockout_key(username.lower()))

def record_failed_attempt(username):
    key= get_cache_key(username)
    attempts=cache.get(key,0) + 1
    cache.set(key,attempts,timeout=LOCKOUT_TIME)
    if attempts>= FAILED_LIMIT:
        cache.set(get_lockout_key(username),True,timeout=LOCKOUT_TIME)
        
        
def reset_failed_attempts(username):
    cache.delete(get_cache_key(username))
    cache.delete(get_lockout_key(username))