Environments:

| | Trigger | Framework | Compiler | DI |
|---|---|:---:|---|---|
| DEV | Manual | PyCharm IDE | Python 2.x-3.y virtual env. configured by PyCharm | "Sources Root" projects are linked by PyCharm. Other dependencies configured in requirements.txt. |
| STAGE | Github Workflows | Tox | Python 2.x-3.y virtual env. created by Tox | Projects are installed by setup.py files linked together by tox.ini configs |
| PROD | Run Addon in Kodi | Kodi | xbmc.python defined by Kodi | Addons are linked together by kodi configured by addon.xml files |