# Troubleshooting

Common issues and solutions for DClaw Code.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-code

# Check logs
kubectl logs -n dclaw-code deployment/dclaw-code-backend

# Check database
kubectl get clusters -n dclaw-code
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
