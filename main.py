from cache.lru import LRUCache, CacheResultStatus


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cache = LRUCache(10)

    for n in range(10):
        # fill cache up to capacity
        cache.put(str(n), n**2)

    result = cache.get("0")             # accessing a value (currently at the tail) put's it at the head of the cache
    if result.status == CacheResultStatus.HIT:
        print(result.value)             # 0

    cache.put("foo", "bar")             # adding a new key removes least recently used "1"
    cache.put("user_id", "1234")        # adding a new key removes least recently used "2"

    result_1 = cache.get("1")
    result_2 = cache.get("2")

    print(result_1.status)              # CacheResultStatus.MISS
    print(result_2.status)              # CacheResultStatus.MISS

    result_foo = cache.get("foo")
    print(result_foo.status)            # CacheResultStatus.MISS

    print(cache.get("user_id").value)   # 1234

