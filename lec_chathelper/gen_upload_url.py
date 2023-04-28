import hmac
import hashlib


file_path = "hello/vu.jpg"
file_size = 824624
token_string = bytearray(f'{file_path} {file_size}', 'utf-8')

token = hmac.new(str.encode("YOqe6JUVReE/iBJPDgSe25JYjD6vnz7b1Y7cRwRB"), token_string, hashlib.sha256).hexdigest()

print(token)