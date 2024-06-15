import hashlib
import random
import time
import struct
import os

# Класс для представления содержимого текста
class TextContent:
    def __init__(self, x):
        self.x = x

    # Метод для вычисления хэш-значения содержимого
    def calc_hash(self):
        hash_val = hashlib.sha256()
        hash_val.update(self.x.encode('utf-8'))
        return hash_val.digest()

# Функция для вычисления хэш корня Меркла
def merkle_root(transactions):
    if len(transactions) == 1:
        return transactions[0]
    new_level = []
    for i in range(0, len(transactions), 2):
        left = transactions[i]
        right = transactions[i + 1] if i + 1 < len(transactions) else left
        new_level.append(hashlib.sha256(left + right).digest())
    return merkle_root(new_level)

# Функция для создания заголовка блока
def create_block_header(merkle_root_hash, previous_block_hash, nonce):
    block_size = 4 + 32 + 32 + 4 + 4  # Размер заголовка блока (байты)
    timestamp = int(time.time())
    header = struct.pack('<I32s32sIII', block_size, previous_block_hash,
                         merkle_root_hash, timestamp, nonce, 0)
    return header

# Функция для поиска подходящего значения nonce
def mine_block(transactions, previous_block_hash):
    nonce = 0
    while True:
        merkle_root_hash = merkle_root([tx.calc_hash() for tx in transactions])
        header = create_block_header(merkle_root_hash, previous_block_hash, nonce)
        block_hash = hashlib.sha256(header).digest()
        if block_hash.hex().startswith('0000'):
            return block_hash.hex(), nonce
        nonce += 1

# Создание списка транзакций размером 226 байт каждая
transactions = [
    TextContent(''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=226))),
    TextContent(''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=226))),
    TextContent(''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=226))),
    TextContent(''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=226)))
]

# Случайный хэш предыдущего блока
previous_block_hash = hashlib.sha256(os.urandom(32)).digest()

# Поиск подходящего блока
block_hash, nonce = mine_block(transactions, previous_block_hash)

# Сохранение блока в файл
with open('block.txt', 'w') as file:
    file.write(f'Block Hash: {block_hash}\n')
    file.write(f'Nonce: {nonce}\n')

print("Block mined successfully!")
