# minesweeper

Minesweeper written in Python with TKinter.

![Screenshot](https://raw.githubusercontent.com/timothy-e/minesweeper/master/minesweeper.png)

Things it solves:

- I was tired of clicking and getting just one cell revealed, because then a guess is required. This version will build a new board if the current board doesn't have an empty space on your first click.

Things it will solve in the future:

- After a game is finished (victory or loss), I want to display the cells cleared per second and mines flagged per second statistic, because my friends had a competition for the best per second stats.
- I'm hoping to add a hint feature.

TODO:

- Clearing the board doesn't end the game yet
- Setting key events for Chording requires TKinter's `focus_set()` which results in a weird black outline on the grid.
- Make the GUI at the top look cleaner.
- Beginner / Normal / Expert modes
