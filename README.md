# Mini Telegram Chat (демо для новичка, Windows)

Это учебный мини-чат в стиле Telegram:
- вход по имени;
- вход в комнату (например, `general`);
- обмен сообщениями в реальном времени через WebSocket.

---

## 0) Что нужно установить на Windows

1. **Python 3.10+**
   - Скачайте с официального сайта: https://www.python.org/downloads/windows/
   - ⚠️ Во время установки обязательно включите галочку **Add Python to PATH**.

2. **Git for Windows**
   - Скачайте: https://git-scm.com/download/win
   - Установите с настройками по умолчанию.

3. **Терминал**
   - Можно использовать **PowerShell** (рекомендуется) или **Windows Terminal**.

Проверка после установки (в новом PowerShell):

```powershell
python --version
git --version
```

Если команды выводят версии — всё ок.

---

## 1) Как запустить проект (пошагово)

### Шаг 1. Откройте папку проекта

Если у вас уже есть папка проекта:

```powershell
cd C:\path\to\C-dev-codex-test
```

### Шаг 2. Создайте и активируйте виртуальное окружение

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Если PowerShell ругается на выполнение скриптов, один раз выполните:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Потом снова:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Шаг 3. Установите зависимости

```powershell
pip install -r requirements.txt
```

### Шаг 4. Запустите приложение

```powershell
python app.py
```

Должно появиться что-то вроде:
- `Running on http://127.0.0.1:5000`

### Шаг 5. Откройте в браузере

Откройте:

- http://127.0.0.1:5000

Для проверки чата откройте **две вкладки** и зайдите с разными именами.

---

## 2) Как нам быть «синхронными» (очень важно)

Чтобы я быстро помогал, присылайте **точно эти данные**:

1. Команду, которую запускали.
2. Полный текст ошибки (лучше скрин или копипасту).
3. Вывод:

```powershell
python --version
pip --version
git status
```

4. Где именно остановились (например: «на шаге активации .venv»).

Удобный формат сообщения мне:

```text
Шаг: 2 (активация venv)
Команда: .\.venv\Scripts\Activate.ps1
Ошибка: ...
```

---


## 2.1) Почему кажется, что мы в «разных окружениях»

Это нормально: фактически у нас **разные машины**.
- Вы запускаете проект у себя на Windows.
- Я проверяю код в отдельном Linux-контейнере.

Поэтому могут отличаться:
- пути (`C:\...` у вас и `/workspace/...` у меня);
- команды активации окружения;
- версии Python/pip;
- системные ошибки ОС.

Чтобы работать как будто в одном окружении, держим синхронизацию по 4 пунктам:

1. Одна и та же папка проекта (где лежат `app.py` и `requirements.txt`).
2. Одинаковая последовательность команд (из этого README).
3. Вы присылаете точный вывод команд ниже.
4. Я даю следующий шаг только после вашего вывода.

Мини-набор для проверки синхронизации (в PowerShell):

```powershell
pwd
dir
python --version
pip --version
```

Если эти 4 команды прислать мне, я сразу скажу, где расхождение и что сделать дальше.

---

## 2.2) Ваш текущий кейс (когда `dir` показывает только `.venv`)

Если в папке видно только `.venv`, как в вашем выводе:

- `Path: C:\dev\codex-test`
- в `dir` есть только `.venv`

то это означает, что в этой папке **нет файлов проекта** (`app.py`, `requirements.txt`, `static/`, `templates/`).

Что сделать:

1. Проверьте, где реально лежит проект:

```powershell
Get-ChildItem C:\dev -Directory
```

2. Перейдите в папку, где есть `requirements.txt`:

```powershell
cd C:\dev\C-dev-codex-test
# или другая папка, где лежит requirements.txt
```

3. Проверьте, что вы точно в нужном месте:

```powershell
dir
```

В выводе должны быть хотя бы:
- `requirements.txt`
- `app.py`
- `templates`
- `static`

4. Только после этого ставьте зависимости:

```powershell
python -m pip install -r requirements.txt
```

Если проекта на диске вообще нет, склонируйте его заново:

```powershell
cd C:\dev
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ> C-dev-codex-test
cd C:\dev\C-dev-codex-test
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

---

## 3) Частые проблемы на Windows

### `python is not recognized`
Python не добавлен в PATH. Переустановите Python с галочкой **Add Python to PATH**.


### `ERROR: Could not open requirements file: ... requirements.txt`
Это значит, что вы запускаете команду **не из папки проекта**.

Проверьте текущую папку:

```powershell
pwd
dir
```

В списке файлов должен быть `requirements.txt`. Если файла не видно — перейдите в папку проекта:

```powershell
cd C:\path\to\C-dev-codex-test
```

После этого снова:

```powershell
pip install -r requirements.txt
```

Можно использовать и абсолютный путь (если всё равно путается папка):

```powershell
pip install -r C:\path\to\C-dev-codex-test\requirements.txt
```

### `pip is not recognized`
Запустите:

```powershell
python -m pip install --upgrade pip
```

И дальше используйте `python -m pip ...`.

### Порт 5000 занят

Запустите на другом порту:

```powershell
python -c "from app import app; app.run(host='0.0.0.0', port=5001, debug=True)"
```

И откройте http://127.0.0.1:5001.

---

## 4) Что это за проект и его ограничения

- Данные хранятся только в памяти процесса (перезапуск = история пропала).
- Нет регистрации/авторизации.
- Нет шифрования, файлов и production-инфраструктуры.
- Это именно учебный прототип.

---

## 5) Как добавить это в ВАШ репозиторий (git add / commit / push)

Если хотите, чтобы изменения оказались в вашем GitHub-репозитории, выполните в PowerShell:

```powershell
cd C:\dev\C-dev-codex-test
git status
git add README.md app.py requirements.txt static templates
git commit -m "Add mini telegram chat demo and Windows onboarding"
git branch
git remote -v
git push origin <ВАША_ВЕТКА>
```

Если репозиторий новый и `origin` ещё не настроен:

```powershell
git remote add origin <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
git push -u origin main
```

Проверка, что всё действительно попало в репозиторий:

```powershell
git log --oneline -n 3
git status
```

Ожидаемо:
- `git status` покажет `nothing to commit, working tree clean`;
- в GitHub появится ваш последний коммит.
