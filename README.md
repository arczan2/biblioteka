# biblioteka
Projekt systemu zarządzania biblioteką na zajęcia z Inżynierii Oprogramowania

# Przygotowanie środowiska developerskiego
Do pracy nad projektem wymagany jest zainstalowany Python w wersji >=3.7 oraz virtualenv.

Na początek musimy pobrać projekt:
```bash
git clone https://github.com/arczan2/biblioteka.git
```
Następinie tworzymy wirtualne środowkisko za pomocą programu virtual env:
```bash
cd biblioteka
virtualenv venv
```
Aktywacji środowisko dokonujemy komendą:
```bash
source venv/bin/activate
```
Po aktywacji virtualenv'a musimy dokonać migracji bazy danych:
```bash
python3 manage.py migrate
```
Ostatnim krokiem jest uruchomienie serwera developerskiego:
```bash
python3 manage.py runserver
```
Gdy wykonamy wszystkie kroki aplikacja jest dostępna pod adresem: localhost:8000
