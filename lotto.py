import random

# ch = [] # 포함할 수
ch = [12, 15, 17, 18, 22, 24, 25, 27, 35, 38, 44, 45]
ch = set(ch)

result = random.sample(ch, 6)
result.sort()
print(result)