# Projekt: Generowanie raportu z analizy logów

## Opis projektu
Celem projektu jest pobranie logów z serwerów, analiza tych logów oraz generowanie raportu w formie dokumentu Word. Raport zawiera szczegółowe dane dotyczące działania komputerów emisyjnych w elektrowni. W szczególności, analizowane są dane o zużyciu CPU, pamięci RAM oraz przestrzeni dyskowej, a także logi systemowe i aplikacyjne.

## Struktura projektu
Projekt składa się z kilku plików, które pełnią różne funkcje:

### 1. **main.py**
Główny plik programu, który:
- Pobiera dane logów z serwera za pomocą SCP.
- Generuje raport na podstawie pobranych danych.
- Usuwa logi po zakończeniu operacji (opcjonalnie, z możliwością wyłączenia tej funkcji).

### 2. **fetch_files.py**
Moduł odpowiedzialny za pobieranie plików logów z serwera za pomocą protokołu SCP. Pobiera logi dla trzech komputerów (SSMS1, SSMS2, SSMS3) na podstawie daty.

### 3. **document_writer.py**
Moduł odpowiedzialny za tworzenie raportu w formacie `.docx`. Generuje dokument, dodaje nagłówki, sekcje analizy logów, obciążenia komputerów, dane dyskowe, wnioski oraz inne niezbędne informacje.

### 4. **data_fetcher.py**
Moduł odpowiedzialny za przetwarzanie plików logów. Parsuje pliki logów i wyciąga dane o dacie restartu, użyciu CPU, RAM, oraz szczegóły dotyczące dysków twardych.

## Jak używać projektu?

### Wymagania
- Python 3.7+
- Zainstalowane biblioteki:
  - `python-docx` - do generowania dokumentów Word
  - `glob` - do przetwarzania plików
  - `math` - do obliczeń matematycznych
  - `subprocess` - do uruchamiania poleceń systemowych (np. SCP)

Zainstaluj wymagane biblioteki za pomocą pip:
```bash
pip install python-docx
```

### Uruchamianie programu
Aby uruchomić program, użyj poniższego polecenia:

```bash
python main.py <rok> <miesiąc> <dzień> [--no-remove]
```

#### Parametry:
- `rok` (int): Rok raportu.
- `miesiąc` (int): Miesiąc raportu (1-12).
- `dzień` (int): Dzień raportu (1-31).
- `--no-remove` (opcjonalnie): Flaga, która zapobiega usunięciu pobranych plików logów po zakończeniu analizy.

Przykład uruchomienia:
```bash
python main.py 2024 11 12
```

Powyższe polecenie wygeneruje raport za 12 listopada 2024 roku, pobierając logi z serwera i zapisując raport do pliku `analiza_logow_2024_11_12.docx`.

### Struktura folderów
Projekt wymaga następującej struktury katalogów:
```
/projekt
│
├── /scripts
│   ├── fetch_files.py
│   ├── data_fetcher.py
│   ├── document_writer.py
├── main.py
```

### Opis działania:
1. **Pobieranie logów**:
   - Program po uruchomieniu łączy się z serwerem (domyślnie `localhost`) i pobiera pliki logów z określoną datą.
   - Logi pobierane są z trzech komputerów (SSMS1, SSMS2, SSMS3) przy użyciu protokołu SCP.

2. **Generowanie raportu**:
   - Po pobraniu danych, program generuje raport w formacie `.docx` zawierający:
     - Nagłówek z nazwą firmy.
     - Datę raportu.
     - Analizę logów z komputerów (w tym informacje o restartach, synchronizacji czasu, logach systemowych i aplikacyjnych).
     - Szczegóły dotyczące obciążenia komputerów oraz przestrzeni dyskowej.
     - Wnioski dotyczące stanu komputerów emisyjnych.

3. **Usuwanie logów**:
   - Po wygenerowaniu raportu program może (jeśli nie użyto flagi `--no-remove`) usunąć pobrane pliki logów, aby nie zajmowały miejsca na dysku.

## Funkcjonalności
### Funkcje dostępne w projekcie:
- **Generowanie raportu** na podstawie logów z serwera.
- **Analiza logów** z komputerów emisyjnych (w tym dane o użyciu CPU, RAM oraz dysków).
- **Generowanie raportu w formacie Word** (z tabelami i tekstami analitycznymi).
- **Usuwanie pobranych plików logów** (po zakończeniu operacji).
