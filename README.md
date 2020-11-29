# biblioteka
Projekt systemu zarządzania biblioteką na zajęcia z Inżynierii Oprogramowania

# Przygotowanie środowiska deweloperskiego
Do pracy nad projektem wymagany jest zainstalowany **Python w wersji >=3.7** oraz **virtualenv**.

Na początek musimy pobrać projekt:
```bash
git clone https://github.com/arczan2/biblioteka.git
```
Następinie tworzymy wirtualne środowkisko za pomocą programu virtualenv:
```bash
cd biblioteka
virtualenv venv
```
Aktywacji środowiska pod linuxem dokonujemy komendą:
```bash
source venv/bin/activate
```
albo pod Windowsem:
```
.\venv\Scripts\activate
```
Po aktywacji virtualenv'a musimy zainstalować wymagane moduły pythona oraz dokonać migracji bazy danych:
```bash
pip install -r requirements.txt
python3 manage.py migrate
```
Ostatnim krokiem jest uruchomienie serwera deweloperskiego:
```bash
python3 manage.py runserver
```
Gdy wykonamy wszystkie kroki aplikacja jest dostępna pod adresem **localhost:8000**

Po zakończeniu prac możemy wyjść z virtualenv'a za pomocą polecenia:
```bash
deactivate
```
