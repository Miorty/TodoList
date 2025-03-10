import redis
import json

"""
r = redis.Redis(host='localhost', port=6379, db=1)
keys = r.keys("*")
# Выводим ключи
print([key.decode("utf-8") for key in keys])  # Декодируем байты в строки
print(keys)

# Получаем последние 10 логов (или все, если их меньше)
logs = r.lrange("http_logs", 0, 9)

#Удаление всех logs
for log in logs:
    r.delete('http_logs')
    
# Декодируем JSON
decoded_logs = [json.loads(log) for log in logs]

print(decoded_logs)
"""

r = redis.Redis(host="localhost", port=6379, db=0)
keys = r.keys("*")
# for key in keys:
#     r.delete(key)
# Выводим ключи
print([key.decode("utf-8") for key in keys])  # Декодируем байты в строки
print(keys)
