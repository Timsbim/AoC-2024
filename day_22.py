print("Day 22")
EXAMPLE = False

file_name = f"2024/input/day_22{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    SECRETS = tuple(int(line.rstrip()) for line in file)
PRUNE = 16777216
    

def next_secret(secret):
    secret = ((secret * 64) ^ secret) % PRUNE
    secret = ((secret // 32) ^ secret) % PRUNE
    return ((secret * 2048) ^ secret) % PRUNE


solution_1, bananas = 0, {}
for secret in SECRETS:
    price, prices, changes = secret % 10, [], []
    for _ in range(2_000):
        secret = next_secret(secret)
        price_new = secret % 10
        changes.append(price_new - price)
        prices.append(price_new)
        price = price_new
    solution_1 += secret
    candidates = set()
    for i in range(3, 2_000):
        sequence = tuple(changes[i-3:i+1])
        if sequence in candidates: continue
        candidates.add(sequence)
        bananas[sequence] = bananas.get(sequence, 0) + prices[i]    

print("Part 1:", solution_1)
print("Part 2:", max(bananas.values()))
assert solution_1 == (37327623 if EXAMPLE else 20068964552)
assert max(bananas.values()) == (24 if EXAMPLE else 2246)
