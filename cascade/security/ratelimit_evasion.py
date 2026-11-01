import asyncio
import time
import random
from collections import defaultdict
from typing import Dict, Optional, Any


class SmartRateLimiter:
    def __init__(self):
        self.buckets: Dict[str, Dict] = defaultdict(lambda: {
            'remaining': 1,
            'reset': 0,
            'limit': 1,
            'last_request': 0
        })
        self.global_rate_limit = False
        self.global_reset = 0.0
        self.request_count = 0
        self.start_time = time.time()
        self._lock = asyncio.Lock()
        
    async def acquire(self, route: str, method: str = 'GET') -> None:
        key = f"{method}:{route}"
        await self.wait_if_needed(key)

    async def wait_if_needed(self, route: str):
        async with self._lock:
            await self._check_global_limit()
            await self._check_bucket_limit(route)
            await self._add_human_delay()
    
    async def _check_global_limit(self):
        if self.global_rate_limit or self.global_reset > 0:
            now = time.time()
            wait_time = self.global_reset - now
            if wait_time > 0:
                jitter = random.uniform(0.1, 0.5)
                await asyncio.sleep(wait_time + jitter)
            self.global_rate_limit = False
            self.global_reset = 0.0
    
    async def _check_bucket_limit(self, route: str):
        bucket = self.buckets[route]
        now = time.time()
        if bucket['remaining'] <= 0 and bucket['reset'] > now:
            wait_time = bucket['reset'] - now
            jitter = random.uniform(0.1, 0.4)
            await asyncio.sleep(wait_time + jitter)
            bucket['remaining'] = bucket.get('limit', 1)
        elif bucket['reset'] <= now:
            bucket['remaining'] = max(bucket.get('remaining', 1), 1)
    
    async def _add_human_delay(self):
        elapsed = time.time() - self.start_time
        requests_per_second = self.request_count / max(elapsed, 1.0)
        
        if requests_per_second > 10:
            await asyncio.sleep(random.uniform(0.3, 0.8))
        elif requests_per_second > 5:
            await asyncio.sleep(random.uniform(0.1, 0.3))
        else:
            await asyncio.sleep(random.uniform(0.02, 0.1))
        
        self.request_count += 1
    
    def update_bucket(self, route: str, method_or_headers: Any, headers: Optional[Dict] = None):
        if isinstance(method_or_headers, dict) and headers is None:
            hdr = method_or_headers
            route_key = route
        else:
            hdr = headers or {}
            route_key = f"{method_or_headers}:{route}"

        bucket = self.buckets[route_key]
        
        if 'X-RateLimit-Remaining' in hdr:
            try:
                bucket['remaining'] = int(hdr['X-RateLimit-Remaining'])
            except (ValueError, TypeError):
                pass
        
        if 'X-RateLimit-Reset' in hdr:
            try:
                bucket['reset'] = float(hdr['X-RateLimit-Reset'])
            except (ValueError, TypeError):
                pass
        
        if 'X-RateLimit-Limit' in hdr:
            try:
                bucket['limit'] = int(hdr['X-RateLimit-Limit'])
            except (ValueError, TypeError):
                pass
        
        bucket['last_request'] = time.time()
        
        if hdr.get('X-RateLimit-Global') in ('true', True):
            self.global_rate_limit = True
            if 'Retry-After' in hdr:
                try:
                    self.global_reset = time.time() + float(hdr['Retry-After'])
                except (ValueError, TypeError):
                    pass
    
    def get_adaptive_delay(self, route: str) -> float:
        bucket = self.buckets[route]
        
        if bucket['limit'] == 0:
            return random.uniform(0.5, 1.5)
        
        usage_ratio = 1 - (bucket['remaining'] / bucket['limit'])
        
        if usage_ratio > 0.9:
            return random.uniform(2.0, 4.0)
        elif usage_ratio > 0.7:
            return random.uniform(1.0, 2.0)
        elif usage_ratio > 0.5:
            return random.uniform(0.5, 1.0)
        else:
            return random.uniform(0.1, 0.5)
