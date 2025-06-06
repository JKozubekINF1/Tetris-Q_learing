# Tetris Q-Learning AI

Projekt "Tetris Q-Learning AI" to implementacja sztucznej inteligencji opartej na algorytmie Q-Learning, umożliwiającej autonomiczne granie w Tetrisa. Celem jest maksymalizacja punktacji, usuwanie linii (szczególnie Tetrisów), minimalizacja dziur oraz utrzymanie stabilnej planszy. AI została opracowana w Pythonie, wykorzystuje bibliotekę Selenium do sterowania grą w JavaScript oraz zmodyfikowaną wersję Tetrisa dostępną na [gist.github.com/straker/3c98304f8a6a9174efd8292800891ea1](https://gist.github.com/straker/3c98304f8a6a9174efd8292800891ea1).

## Funkcjonalności
- **Q-Learning**: AI uczy się strategii gry poprzez iteracyjne aktualizacje tabeli Q, stosując strategię ε-greedy.
- **System nagród i kar**: Promuje usuwanie linii (+1000 do +4000), karze za dziury (-300 * holes) i nierówności (-15 * bumpiness).
- **Integracja z grą**: Selenium umożliwia komunikację między Pythonem a grą w JavaScript.
- **Metryki planszy**: Ocena stanu gry na podstawie *completeness*, *holes*, *bumpiness* i *max_height*.

## Wymagania
- **Python**: 3.9+
- **Biblioteki**: NumPy, TensorFlow, Selenium
- **Node.js**: Do uruchamiania gry
- **Przeglądarka**: Chrome lub Firefox

## Uruchomienie
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/JKozubekINF1/Tetris-Q_learning.git
