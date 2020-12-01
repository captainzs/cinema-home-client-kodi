<h1 align="center">
  Cinema Home - In-House Movie Streaming Environment
  <h2 align="center">
  Kodi Client
  </h21>
</h1>

<p align="center">
  <a href="LICENSE.md"><img alt="License" src="https://img.shields.io/badge/License-GPLv3-brightgreen"></a>
  <a><img alt="code" src="https://img.shields.io/badge/code-clean-blue"></a>
  <a href="https://github.com/captainzs/cinema-home-client-kodi/pulls"><img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-yellowgreen"></a>
  <a href="https://github.com/captainzs/cinema-home-client-kodi/actions"><img alt="Build" src="https://img.shields.io/badge/CI-github-orange"></a>
</p>

<p align="center">
  <img src="docs/screenshots.gif" alt="Screenshots">
</p>

## Contents:
1. [ Overview ](#overview)
2. [ Install ](#install)
3. [ Install Server ](#server)
4. [ Development ](#dev)
    1. [ Development Environments ](#envs)

<a name="overview"></a>
## 1. Overview
 Cinema-Home is a software system that lets you enjoy movies and tv-shows for free. With seemlessly integrating to third-party media softwares (TMDB, IMDB, Fanart.tv) Cinema-Home works just like your favorite paid streaming service, like Netflix or HBO. Movies and tv-shows are downloaded through torrent-trackers with no user interactions at all.
 
<a name="install"></a>
## 2. Install
This **kodi addon** can be installed through my [kodi-artifact-repository](https://github.com/captainzs/repository.cinema.home). 

<a name="server"></a>
## 3. Install Server
You can fine detailed instructions about installing the server component for this software [in my repository](https://github.com/captainzs/cinema-home-server).

<a name="dev"></a>
## 4. Development
You can fork and redevelop my addon under the license terms.
<a name="envs"></a>
### 4.1 Development Environments
| | Trigger | Framework | Compiler | DI |
|---|---|:---:|---|---|
| DEV | Manual | IDE (PyCharm) | Python 2.x-3.y virtual env. configured by PyCharm | "Sources Root" projects are linked by your IDE. Other dependencies configured in requirements.txt. |
| STAGE | Github Workflows | Tox | Python 2.x-3.y virtual env. created by Tox | Projects are installed by setup.py files linked together by tox.ini configs |
| PROD | Run Addon in Kodi | Kodi | xbmc.python defined by Kodi | Addons are linked together by kodi configured by addon.xml files |

### License
Cinema-Home kodi client is [GPLv3 licensed](https://github.com/captainzs/cinema-home-server/blob/main/LICENSE). You may use, distribute and copy it under the license terms.



