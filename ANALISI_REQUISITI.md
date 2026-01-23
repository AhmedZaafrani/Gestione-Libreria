# Analisi dei Requisiti

## Cosa deve fare il progetto

Il progetto serve per gestire una libreria. Praticamente puoi vedere i libri, cercarne qualcuno, aggiungerne di nuovi e cancellarli. È tipo un database ma più facile da usare.

## Requisiti Funzionali

### Cosa deve fare l'applicazione:

1. **Vedere i libri**
   - Deve mostrare tutti i libri che ci sono
   - Ogni libro ha: titolo, autore, genere, anno e ISBN
   - Si vedono tipo in delle scatoline

2. **Cercare libri**
   - C'è una barra di ricerca dove scrivi il nome dell'autore
   - Ti filtra solo quelli che vuoi tu

3. **Aggiungere libri**
   - Sotto c'è un form dove scrivi titolo, autore e genere
   - Premi "Aggiungi" e il libro si aggiunge alla lista

4. **Cancellare libri**
   - Ogni libro ha una X per cancellarlo
   - C'è anche un bottone per cancellare tutto insieme

5. **Generare libri casuali**
   - C'è un bottone "Genera" che crea 5 libri a caso
   - Utile per fare prove

## Requisiti Non Funzionali

### Come deve funzionare:

- **Velocità**: Deve essere veloce, non deve fare aspettare troppo
- **Facile da usare**: Anche mia nonna deve capire come funziona
- **Bello da vedere**: Colori scuri ma non troppo, tipo moderno
- **Funziona sempre**: Non deve crashare se sbagli qualcosa

## Requisiti Tecnici

### Backend (la parte nascosta):
- Python con Flask
- Genera dati finti con Faker
- API REST per comunicare col frontend

### Frontend (quello che si vede):
- React per l'interfaccia
- Vite per renderlo veloce
- Design responsive (funziona anche sul telefono)

## Limiti e Vincoli

- I dati non vengono salvati per sempre, quando spegni tutto si perdono
- Massimo 100 libri generati alla volta
- Cerca solo per autore, non per titolo
- Internet necessario per far funzionare tutto
