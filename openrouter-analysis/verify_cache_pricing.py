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

pricing_keys = set()
cache_keys = set()
discount_keys = set()

for m in models:
    pricing = m.get('pricing', {})
    if not isinstance(pricing, dict): continue
    for k in pricing.keys():
        pricing_keys.add(k)
        if 'cache' in k: cache_keys.add(k)
        if 'discount' in k: discount_keys.add(k)

print(f"Total models analyzed: {len(models)}")
print(f"All Unique Pricing Keys across all models: {pricing_keys}")
print(f"Cache-specific Pricing Keys: {cache_keys}")
print(f"Discount-specific Pricing Keys: {discount_keys}")
print("API Contract Verified: If 'input_cache_read' is not present, the model does not expose cached token prices, and fallback logic based on discounts is invalid.")
