# Sepsis Application Backend
## How to run this?
* **Step1:** Create virtual environment in shell:
```bash
python -m venv .venv
# access to the venv
# run the command activate.your_shell_ext based on your shell
source ./.venv/bin/activate
```

* **Step2:** Install required dependencies:
```bash
pip install -r requirements.txt
```

* **Step3:** Run the project in dev environment:
```bash
fastapi dev src/main.py
```

## The structure:
### File structure:
```
src/
├── main.py                  # Application entrypoint
├── api/                     # Everything API-related (controllers = routers, services = business logic)
│   ├── __init__.py
│   └── account/             # Features based
│        ├ getAll.py         # All routes related to get accounts (They can be get all accounts, get a account, ...)
│        └ ...
│
├── repositories/            # Everything Database-related (Table definitions = Models, Query)
│   ├── __init__.py
│   ├── account.py           # Account models
│   └── ...
```
