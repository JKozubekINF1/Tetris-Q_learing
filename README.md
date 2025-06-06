# Tetris Q-Learning AI

Projekt "Tetris Q-Learning AI" to implementacja sztucznej inteligencji opartej na algorytmie Q-Learning, umożliwiającej autonomiczne granie w Tetrisa. Celem jest maksymalizacja punktacji, usuwanie linii (szczególnie Tetrisów), minimalizacja dziur oraz utrzymanie stabilnej planszy. AI została opracowana w Pythonie, wykorzystuje bibliotekę Selenium do sterowania grą w JavaScript oraz zmodyfikowaną wersję Tetrisa dostępną na [gist.github.com/straker/3c98304f8a6a9174efd8292800891ea1](https://gist.github.com/straker/3c98304f8a6a9174efd8292800891ea1).

## Funkcjonalności
- **Q-Learning**: AI uczy się strategii gry poprzez iteracyjne aktualizacje tabeli Q, stosując strategię ε-greedy.
- **System nagród i kar**: Promuje usuwanie linii (+1000 do +4000), karze za dziury (-300 * holes) i nierówności (-15 * bumpiness).
- **Integracja z grą**: Selenium umożliwia komunikację między Pythonem a grą w JavaScript.
- **Metryki planszy**: Ocena stanu gry na podstawie *completeness*, *holes*, *bumpiness* i *max_height*.

## Wymagania
- **Python**: 3.9+
- **Biblioteki**: NumPy, Selenium, matplotlib
- **Przeglądarka**: Chrome lub Firefox

## Uruchomienie
Należy zainstalować projekt AI do grania w tetrisa:
```bash
git clone https://github.com/JKozubekINF1/Tetris-Q_learing
```

Przejdź do nowo utworzonego folderu:
```bash
cd Tetris-Q_learing
```

Następnie zainstalować zależności:
```bash
pip install numpy matplotlib selenium
```

Aby zacząć grę w tetrisa należy uruchomić play_tetris.py:
```bash
python play_tetris.py
```
