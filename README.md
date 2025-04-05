# 🧩 browserstate-nova-adapter

This package makes it easy to use [BrowserState](https://github.com/browserstate-org/browserstate) with [Amazon Nova Act](https://labs.amazon.science/blog/nova-act). It ensures persistent browser memory across Nova sessions by mounting and unmounting full `user_data_dir` browser state.

> Store and restore cookies, localStorage, IndexedDB, and more — across runs, machines, and cloud environments.

---


## 📦 Install (Coming Soon)

> This package is under active development and will be published to PyPI soon. In the meantime, clone or install directly from source if you're contributing or testing.

---

---

## 🚀 Quickstart Example (Nova + BrowserState)

```python
from browserstate_nova_adapter import with_browserstate
from nova_act import NovaAct

with with_browserstate(
    user_id="demo-user",
    state_id="nova-session",
    provider="redis",  # or 'local', 's3', 'gcs'
    redis_options={"host": "localhost", "port": 6379}
) as user_data_dir:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")
```

---

## 🔧 Manual Usage

```python
from browserstate_nova_adapter import mount_browserstate, unmount_browserstate
from nova_act import NovaAct

user_data_dir = mount_browserstate(
    user_id="demo",
    state_id="session1",
    provider="local"
)

try:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")
finally:
    unmount_browserstate()
```

---

## 🌍 Storage Providers
- Local (default)
- Redis (with TTL, keyPrefix)
- AWS S3 *(experimental)*
- Google Cloud Storage *(experimental)*

---

## 🔗 Related Projects
- [BrowserState Core](https://github.com/browserstate-org/browserstate)
- [Nova Act](https://labs.amazon.science/blog/nova-act)

---

## 🤝 Contributing
PRs welcome — especially if you’re using BrowserState with other automation tools.

---

## ⚖️ License
MIT

---

## 🧠 Why this exists
Nova sessions reset browser context every run.
This adapter makes Nova Act automations behave like real users — with memory.
It wraps `BrowserState`'s mounting logic, handles cleanup, and supports Redis/S3/local/gcs.
