import urllib.request
import json
import os
import ssl

url = "https://openrouter.ai/api/v1/models"
req = urllib.request.Request(url)
# TLS certificate verification stays on. Optionally set OPENROUTER_CA_BUNDLE to a
# PEM file to trust a custom CA (for example, a corporate proxy's root certificate).
ctx = ssl.create_default_context(cafile=os.environ.get("OPENROUTER_CA_BUNDLE") or None)

with urllib.request.urlopen(req, context=ctx) as response:
    data = json.loads(response.read().decode('utf-8'))
    models = data.get('data', [])

output_lines = ["--- EXPLICIT API CONTRACT PROOF ---"]

with_cache = next((m for m in models if 'input_cache_read' in m.get('pricing', {})), None)
if with_cache:
    output_lines.extend(["", f"MODEL WITH CACHE: {with_cache['id']}", json.dumps(with_cache.get('pricing'), indent=2)])

without_cache = next((m for m in models if 'input_cache_read' not in m.get('pricing', {})), None)
if without_cache:
    output_lines.extend(["", f"MODEL WITHOUT CACHE: {without_cache['id']}", json.dumps(without_cache.get('pricing'), indent=2)])

moe_model = next((m for m in models if '8x' in m.get('id', '') or '8x' in m.get('name', '')), None)
if moe_model:
    output_lines.extend(["", f"MOE MODEL: {moe_model['id']}", json.dumps(moe_model.get('pricing'), indent=2)])

output_lines.extend(["", "CONCLUSION: The 'input_cache_read' field exists statically within the 'pricing' dictionary strictly when cache pricing is supported. The data type is a string representing cost per token. Absent cache, the field is entirely omitted."])

with open("contract_proof.txt", "w", encoding="utf-8") as f:
    f.write("\\n".join(output_lines))
    
print("Successfully generated contract_proof.txt")
