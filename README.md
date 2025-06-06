
Tetris Q-Learning AI
Projekt "Tetris Q-Learning AI" to implementacja sztucznej inteligencji opartej na algorytmie Q-Learning do autonomicznego grania w Tetrisa. Celem jest maksymalizacja punktacji, usuwanie linii (szczególnie Tetrisów), minimalizacja dziur i utrzymanie stabilnej planszy. AI wykorzystuje Pythona, bibliotekę Selenium do sterowania grą w JavaScript oraz zmodyfikowaną wersję Tetrisa z gist.github.com/straker/3c98304f8a6a9174efd8292800891ea1.

Funkcjonalności
Q-Learning: AI uczy się strategii gry poprzez iteracyjne aktualizacje tabeli Q, stosując strategię ε-greedy.
System nagród i kar: Promuje usuwanie linii (+1000 do +4000), karze za dziury (-300 * holes) i nierówności (-15 * bumpiness).
Integracja z grą: Selenium umożliwia komunikację między Pythonem a grą w JavaScript.
Metryki planszy: Ocena stanu gry na podstawie completeness, holes, bumpiness i max_height.
Wymagania
Python 3.9+
Biblioteki: NumPy, TensorFlow, Selenium
Node.js (do uruchamiania gry)
Przeglądarka: Chrome/Firefox
Gra Tetris w JavaScript
Uruchomienie
Sklonuj repozytorium: git clone https://github.com/JKozubekINF1/Tetris-Q_learning.git
Zainstaluj zależności: pip install -r requirements.txt
Uruchom AI: python play_tetris.py
