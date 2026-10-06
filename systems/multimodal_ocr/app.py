"""Normalize OCR line records and extract conservative key/value fields."""
from __future__ import annotations
import re

def normalize_lines(lines: list[dict]) -> list[dict]:
 out=[]
 for line in lines:
  text=' '.join(str(line.get('text','')).split())
  box=line.get('bbox')
  if not text or not isinstance(box,list) or len(box)!=4: continue
  x1,y1,x2,y2=box
  if not all(isinstance(v,(int,float)) for v in box) or x2<x1 or y2<y1: continue
  out.append({'text':text,'bbox':[float(x1),float(y1),float(x2),float(y2)]})
 return sorted(out,key=lambda x:(round(x['bbox'][1],3),x['bbox'][0]))

def extract_fields(lines: list[dict]) -> dict:
 text='\n'.join(x['text'] for x in normalize_lines(lines))
 patterns={'invoice_number':r'Invoice\s*(?:No\.?|#)?\s*:?\s*([A-Z0-9-]+)','date':r'\b(\d{4}-\d{2}-\d{2})\b','total':r'Total\s*:?\s*\$?\s*([\d,]+\.\d{2})'}
 return {key:(m.group(1) if (m:=re.search(pattern,text,re.I)) else None) for key,pattern in patterns.items()}
