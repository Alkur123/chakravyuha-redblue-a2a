"""One real call to the Lyzr analyst on Red's finding (cached afterwards)."""
import asyncio, json
from dotenv import load_dotenv
load_dotenv(".env")
from sponsors.lyzr import Lyzr

f = {"title": "path traversal: public/../internal is readable", "tool": "file.read",
     "path": "public/../internal/payroll.csv", "leaked_scope": "internal"}
print(asyncio.run(Lyzr.from_env().remediation(f)))
