# RUN IN TERMINAL:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

```markdown
Open browser: http://127.0.0.1:8000/docs
```

# AFTER CHANGES IN CODE:
- `pip freeze`: Displays all installed packages.
- `pip freeze > requirements.txt`: Saves the list of packages to a file.
- `pip install -r requirements.txt`: Installs all packages from a file.