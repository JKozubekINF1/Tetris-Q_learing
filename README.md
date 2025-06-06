Tetris Q-Learning AI
Projekt "Tetris Q-Learning AI" to implementacja sztucznej inteligencji opartej na algorytmie Q-Learning, umożliwiającej autonomiczne granie w Tetrisa. Celem jest maksymalizacja punktacji, usuwanie linii (szczególnie Tetrisów), minimalizacja dziur oraz utrzymanie stabilnej planszy. AI została opracowana w Pythonie, wykorzystuje bibliotekę Selenium do sterowania grą w JavaScript oraz zmodyfikowaną wersję Tetrisa dostępną na gist.github.com/straker/3c98304f8a6a9174efd8292800891ea1.

Funkcjonalności
Q-Learning: AI uczy się strategii gry poprzez iteracyjne aktualizacje tabeli Q, stosując strategię ε-greedy.
System nagród i kar: Promuje usuwanie linii (+1000 do +4000), karze za dziury (-300 * holes) i nierówności (-15 * bumpiness).
Integracja z grą: Selenium umożliwia komunikację między Pythonem a grą w JavaScript.
Metryki planszy: Ocena stanu gry na podstawie completeness, holes, bumpiness i max_height.
Wymagania
Python: 3.9+
Biblioteki: NumPy, TensorFlow, Selenium
Node.js: Do uruchamiania gry
Przeglądarka: Chrome lub Firefox
Gra Tetris w JavaScript: Dostępna pod linkiem
Uruchomienie
Sklonuj repozytorium:
text

Zwiń

Zwiń

Kopiuj
git clone https://github.com/JKozubekINF1/Tetris-Q_learning.git
Zainstaluj zależności:
text

Zwiń

Zwiń

Kopiuj
pip install -r requirements.txt
Uruchom AI:
text

Zwiń

Zwiń

Kopiuj
python play_tetris.py
Dodatkowe uwagi
Upewnij się, że używasz wirtualnego środowiska (np. venv) dla lepszej izolacji zależności.
W przypadku problemów z instalacją bibliotek, upewnij się, że masz zainstalowane narzędzia build (np. Visual Studio Build Tools na Windowsie).
Szczegółowe wyniki i parametry można znaleźć w plikach projektu, takich jak q_table.json i training_results.png.
