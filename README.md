# Gestione Libreria

Sistema di gestione libreria con Flask backend e React frontend.

## Setup

### Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd mP
npm install
npm run dev
```

## Uso

- **Genera**: Crea 5 nuovi libri casuali
- **Mostra tutti**: Carica tutti i libri salvati
- **Cancella tutto**: Rimuove tutti i libri
- **Cerca**: Filtra per nome autore
- **Aggiungi**: Inserisci un nuovo libro manualmente

## Tecnologie

- Backend: Flask, Faker
- Frontend: React, Vite
