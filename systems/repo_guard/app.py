"""A local repository-health check for obvious dangerous configuration."""
from __future__ import annotations
import re
from pathlib import Path

SECRET_PATTERNS=[('private key',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),('AWS access key',re.compile(r'\bAKIA[0-9A-Z]{16}\b'))]
DANGEROUS_ACTIONS=re.compile(r'\b(?:chmod\s+777|curl\s+[^|]+\|\s*(?:sudo\s+)?sh|rm\s+-rf\s+/|eval\s+\$\()',re.I)

def scan(root:Path,ignore:set[str]|None=None)->list[dict]:
 ignore=ignore or {'.git','.venv','venv','node_modules','__pycache__'}; findings=[]
 for path in root.rglob('*'):
  if not path.is_file() or any(part in ignore for part in path.relative_to(root).parts): continue
  try: text=path.read_text(errors='ignore')
  except OSError: continue
  for number,line in enumerate(text.splitlines(),1):
   for label,pattern in SECRET_PATTERNS:
    if pattern.search(line): findings.append({'file':str(path.relative_to(root)),'line':number,'kind':label})
   if path.suffix in {'.sh','.yml','.yaml'} and DANGEROUS_ACTIONS.search(line): findings.append({'file':str(path.relative_to(root)),'line':number,'kind':'dangerous shell pattern'})
 return findings
