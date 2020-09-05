import hashlib
import bcrypt
import hmac

_builtin_safe_str_cmp = getattr(hmac, "compare_digest", None)

def generate_password_hash(password, rounds=None):
    return Bcrypt().generate_password_hash(password, rounds)

def check_password_hash(pw_hash, password):
    return Bcrypt().check_password_hash(pw_hash, password)


def safe_str_cmp(a: str, b: str):
    if isinstance(a, str):
        a = a.encode("utf-8")  # type: ignore
    if isinstance(b, str):
        b = b.encode("utf-8")  # type: ignore

    if _builtin_safe_str_cmp is not None:
        return _builtin_safe_str_cmp(a, b)

    if len(a) != len(b):
        return False
    rv = 0
    for x, y in zip(a, b):
        rv |= x ^ y  # type: ignore

    return rv == 0

class Bcrypt(object):

    _log_rounds = 12
    _prefix = '2b'
    _handle_long_passwords = False

    def _unicode_to_bytes(self, unicode_string):
        '''Converts a unicode string to a bytes object.
        :param unicode_string: The unicode string to convert.'''

        if isinstance(unicode_string, str):
            bytes_object = bytes(unicode_string, 'utf-8')
        else:
            bytes_object = unicode_string

        return bytes_object

    def generate_password_hash(self, password, rounds=None, prefix=None):
        if not password:
            raise ValueError('Password must be non-empty.')

        if rounds is None:
            rounds = self._log_rounds
        if prefix is None:
            prefix = self._prefix

        # Python 3 unicode strings must be encoded as bytes before hashing.
        password = self._unicode_to_bytes(password)
        prefix = self._unicode_to_bytes(prefix)

        if self._handle_long_passwords:
            password = hashlib.sha256(password).hexdigest()
            password = self._unicode_to_bytes(password)

        salt = bcrypt.gensalt(rounds=rounds, prefix=prefix)
        return bcrypt.hashpw(password, salt)

    def check_password_hash(self, pw_hash, password):
        '''Tests a password hash against a candidate password. The candidate 
        password is first hashed and then subsequently compared in constant 
        time to the existing hash. This will either return `True` or `False`.
        Example usage of :class:`check_password_hash` would look something 
        like this::
            pw_hash = bcrypt.generate_password_hash('secret', 10)
            bcrypt.check_password_hash(pw_hash, 'secret') # returns True
        :param pw_hash: The hash to be compared against.
        :param password: The password to compare.
        '''

        # Python 3 unicode strings must be encoded as bytes before hashing.
        pw_hash = self._unicode_to_bytes(pw_hash)
        password = self._unicode_to_bytes(password)

        if self._handle_long_passwords:
            password = hashlib.sha256(password).hexdigest()
            password = self._unicode_to_bytes(password)

        return safe_str_cmp(bcrypt.hashpw(password, pw_hash), pw_hash)