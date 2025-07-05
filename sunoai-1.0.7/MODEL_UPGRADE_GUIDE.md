# MODEL UPGRADE GUIDE

Welcome to the Model Upgrade Guide for `sunoai-1.0.7`. This document will help you upgrade your models to be compatible with the latest version.

---

## 1. Backup Your Data

Before starting, **backup your models and configuration files**.

---

## 2. Review Release Notes

Check the `CHANGELOG.md` for breaking changes and new features introduced in `1.0.7`.

---

## 3. Update Dependencies

Ensure all required dependencies are updated:

```bash
pip install -r requirements.txt --upgrade
```

---

## 4. Update Model Files

- **Model Format Changes:**  
    If the model file format has changed, use the provided migration script:

    ```bash
    python scripts/upgrade_model.py --input old_model.pth --output new_model.pth
    ```

- **Configuration Updates:**  
    Update your configuration files to match new schema requirements. Refer to `config.example.yaml` for reference.

---

## 5. Test the Upgrade

- Run unit tests to verify model integrity.
- Use sample data to ensure predictions are consistent.

---

## 6. Troubleshooting

- Check logs for errors during loading or inference.
- Consult the FAQ section in the documentation for common issues.

---

## 7. Need Help?

If you encounter issues, open an issue on the [GitHub repository](https://github.com/your-repo/sunoai/issues) or contact support.

---

**Thank you for upgrading to `sunoai-1.0.7`!**