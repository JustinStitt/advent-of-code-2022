import sys
import hashlib

inp = sys.stdin.readline().rstrip()

for x in range(2**32):
    concat = inp + str(x)
    result = hashlib.md5(concat.encode()).hexdigest()
    if result[:6] == "0" * 6:
        print("found: ", x)
        print(result)
        sys.exit(1)

print("not found")
