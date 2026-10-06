"""A bounded TTL LRU cache with normalized keys and hit/miss accounting."""
from __future__ import annotations
import hashlib
import time
from collections import OrderedDict
from dataclasses import dataclass

@dataclass
class Entry:
 value: str
 expires_at: float

class SemanticCache:
 """Exact normalized-query cache (no embeddings, API calls, or false semantic match)."""
 def __init__(self,max_entries:int=100,ttl_seconds:float=300,clock=time.monotonic):
  if max_entries<1 or ttl_seconds<=0: raise ValueError('max_entries and ttl_seconds must be positive')
  self.max_entries=max_entries; self.ttl_seconds=ttl_seconds; self.clock=clock; self.data=OrderedDict(); self.hits=0; self.misses=0
 @staticmethod
 def key(query:str,model:str='default',version:str='1') -> str:
  normalized=' '.join(query.casefold().split())
  return hashlib.sha256(f'{model}\0{version}\0{normalized}'.encode()).hexdigest()
 def get(self,query:str,model:str='default',version:str='1') -> str|None:
  key=self.key(query,model,version); entry=self.data.get(key)
  if entry is None or entry.expires_at<=self.clock():
   if entry is not None: del self.data[key]
   self.misses+=1; return None
  self.data.move_to_end(key); self.hits+=1; return entry.value
 def put(self,query:str,value:str,model:str='default',version:str='1') -> None:
  key=self.key(query,model,version); self.data[key]=Entry(value,self.clock()+self.ttl_seconds); self.data.move_to_end(key)
  while len(self.data)>self.max_entries: self.data.popitem(last=False)
 def stats(self):
  total=self.hits+self.misses
  return {'entries':len(self.data),'hits':self.hits,'misses':self.misses,'hit_rate':self.hits/total if total else 0}
