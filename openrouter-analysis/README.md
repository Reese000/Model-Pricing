# OpenRouter Analysis: cache-pricing checks

Scripts and data for checking how the public OpenRouter models API (`https://openrouter.ai/api/v1/models`) exposes cache-read pricing.

## Files

- `verify_cache_pricing.py`: fetches the models API and lists every pricing key that appears across models. It reports which keys contain "cache" or "discount". Use it to confirm whether `input_cache_read` is present.
- `prove_cache_contract.py`: fetches the same API and writes `contract_proof.txt` in the current directory. The file shows sample pricing objects for a model with cache pricing, one without, and one MoE model.
- `unmatched_models.csv`: a snapshot of models that have cache pricing but no matching Artificial Analysis score. It is intended for manual review. It was produced by an earlier coverage pass; the script that wrote it is not included here.

## Usage

```bash
python verify_cache_pricing.py
python prove_cache_contract.py
```

Both scripts need only the Python standard library. They make an unauthenticated GET request, so no API key is required.

## TLS configuration

Certificate verification is on by default. If you are behind a proxy that uses a custom root CA, point the scripts at its PEM bundle:

```bash
export OPENROUTER_CA_BUNDLE=/path/to/ca-bundle.pem
python verify_cache_pricing.py
```
