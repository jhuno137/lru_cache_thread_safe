from collections import OrderedDict
from enum import Enum, auto
import threading


class CacheResultStatus(Enum):
	"""
	Cache request status can be either hit or miss
	"""
	MISS = auto()
	HIT = auto()


class CacheResult:
	"""
	Cache result wrapper, status will indicate whether the request was successful (hit) or not (miss) and
	value will contain the cache value for successful requests.
	"""
	def __init__(self, status: CacheResultStatus, value=None):
		self.status = status
		self.value = value


class LRUCache:
	"""
	Thread safe implementation of LRU cache using an Ordered dictionary
	"""
	def __init__(self, capacity: int):
		self._cache = OrderedDict()
		self._capacity = capacity
		self._lock = threading.Lock()

	def get(self, key: str) -> CacheResult:
		"""
		Get an element from the cache
		:param key:
		:return:
		"""
		if key in self._cache:
			value = self._cache[key]
			self._cache.pop(key)
			self._cache[key] = value
			return CacheResult(CacheResultStatus.HIT, value)
		return CacheResult(CacheResultStatus.MISS)

	def put(self, key: str, value) -> None:
		"""
		Add or update an element from the cache. If the cache reaches maximum capacity and a new element
		is set to be added, then pop the last element from the cache (least recently used).
		:param key:
		:param value:
		:return:
		"""
		if key in self._cache:
			self._cache.pop(key)
			self._cache[key] = value
		else:
			with self._lock:
				# remove least recently used item if cache goes over capacity
				if len(self._cache) >= self._capacity:
					# last=False for objects returned in FIFO order
					self._cache.popitem(last=False)

			self._cache[key] = value

	def delete(self, key: str) -> None:
		"""
		Delete one item from the cache given it's key (if exists)
		:param key:
		:return:
		"""
		with self._lock:
			if key in self._cache:
				self._cache.pop(key)

	def reset(self) -> None:
		"""
		Clear the cache
		:return:
		"""
		self._cache.clear()

