import random
from enum import Enum
import tkinter as tk
from datetime import datetime

CELL_WIDTH = 36
WINDOW_MARGIN = 2 * CELL_WIDTH


class UncoverStatus(Enum):
    NUMBER = 0
    EMPTY = 1
    MINE = 2


class Paint:
    _revealed_bg_light = "#F2F2F2"
    _revealed_bg = "#EEEEEE"
    _revealed_bg_dark = "#EAEAEA"

    _concealed_bg_light = "#DDDDDD"
    _concealed_bg = "#CCCCCC"
    _concealed_bg_dark = "#BBBBBB"
    _text_colors = [
        _revealed_bg,  # 0
        "#1874cd",  # 1
        "#458b00",  # 2
        "#ff4500",  # 3
        "#68228b",  # 4
        "#8b1a1a",  # 5
        "#00c5cd",  # 6
        "#111111",  # 7
        "#828282",  # 8
    ]

    @classmethod
    def _draw_rect(cls, canvas, x, y, *, color, nw_color, se_color):
        """
        Draws a rectangle with top left corner at (x, y) and side lengths of
        CELL_WIDTH.
        Params:
            canvas: the master canvas
            x: the top left corner's x position
            y: the top left corner's y position
            color: the color inside the rectangle
            nw_color: the color of the rectangle NW side
            se_color: the color of the rectangle's SE side
        """
        depth = 0.1
        canvas.create_rectangle(x, y, x + CELL_WIDTH, y + CELL_WIDTH, fill=color, width=0)
        canvas.create_polygon(
            x,
            y,
            x,
            y + CELL_WIDTH * 1.0,
            x + CELL_WIDTH * depth,
            y + CELL_WIDTH * (1 - depth),
            x + CELL_WIDTH * depth,
            y + CELL_WIDTH * depth,
            x + CELL_WIDTH * (1 - depth),
            y + CELL_WIDTH * depth,
            x + CELL_WIDTH,
            y,
            fill=nw_color,
            width=0,  # no border
        )
        canvas.create_polygon(
            x + CELL_WIDTH,
            y + CELL_WIDTH,
            x + CELL_WIDTH,
            y,
            x + CELL_WIDTH * (1 - depth),
            y + CELL_WIDTH * depth,
            x + CELL_WIDTH * (1 - depth),
            y + CELL_WIDTH * (1 - depth),
            x + CELL_WIDTH * depth,
            y + CELL_WIDTH * (1 - depth),
            x,
            y + CELL_WIDTH,
            fill=se_color,
            width=0,  # no border
        )

    @classmethod
    def _draw_text(cls, canvas, x, y, *, text, color):
        """
        Draws a colored string centered in a square starting at (x, y) with
        side length CELL_WIDTH.
        Params:
            canvas: the master canvas
            x: the top left x position of the text
            y: the top left y position of the text
            text: the string to be printed
            color: the text color
        """
        canvas.create_text(x + CELL_WIDTH / 2, y + CELL_WIDTH / 2, fill=color, text=text)

    @classmethod
    def mine(cls, canvas, x, y):
        """
        Draws a mine on the tile at (x, y).
        """
        pass

    @classmethod
    def concealed(cls, canvas, x, y):
        """
        Draws the default tile at (x, y).
        Params:
            canvas: the master canvas
            x: the top left corner's x position
            y: the top left corner's y position
        """

        Paint._draw_rect(
            canvas,
            x,
            y,
            color=Paint._concealed_bg,
            nw_color=Paint._concealed_bg_light,
            se_color=Paint._concealed_bg_dark,
        )

    @classmethod
    def revealed(cls, canvas, x, y, *, count):
        """
        Draws a number with a background at (x, y), used for revealed / empty
        cells.
        Params:
            canvas: the master canvas
            x: the top left corner's x position
            y: the top left corner's y position
            text: the cell count or empty string
            text_color: the hex color of the text
        """
        Paint._draw_rect(
            canvas,
            x,
            y,
            color=Paint._revealed_bg,
            nw_color=Paint._revealed_bg_dark,
            se_color=Paint._revealed_bg_light
        )
        Paint._draw_text(canvas, x, y, text=count, color=Paint._text_colors[count])

    @classmethod
    def flagged(cls, canvas, x, y):
        """
        Draws a flag in the cell starting at (x, y).
        Params:
            canvas: the master canvas
            x: the top left corner's x position
            y: the top left corner's y position
        """
        Paint._draw_rect(canvas, x, y, color="#991111", nw_color="#AA4400", se_color="#882222")


class Cell:
    def __init__(self, canvas, *, row, col):
        self.canvas = canvas
        self.x = row * CELL_WIDTH
        self.y = col * CELL_WIDTH
        Paint.concealed(self.canvas, self.x, self.y)

        self.is_mine = False
        self.uncovered = False
        self.neighbours = []
        self.flagged = False

    def update_count(self):
        self.count = sum(cell.is_mine for cell in self.neighbours)

    def add_neighbour(self, cell):
        self.neighbours.append(cell)

    def uncover(self):
        """
        Returns a `UncoverStatus` enum or `None` if already uncovered
        """
        if self.uncovered:
            return None

        self.uncovered = True
        if self.is_mine:
            Paint.mine(self.canvas, self.x, self.y)
            return UncoverStatus.MINE

        Paint.revealed(self.canvas, self.x, self.y, count=self.count)
        if self.count == 0:
            for neighbour in self.neighbours:
                neighbour.uncover()
            return UncoverStatus.EMPTY
        return UncoverStatus.NUMBER

    def chord(self):
        """
        Chording is a middle-click mouse event that, on a number, if that
        number is satisfied (i.e. surrounded by the correct number of flags),
        then it clears all the surrounding unflagged cells.
        """
        pass

    def flag(self):
        """
        Returns 1 if a cell is flagged, -1 if a cell is unflagged, and 0 if
        nothing happens.
        """
        if self.flagged:
            self.flagged = False
            Paint.concealed(self.canvas, self.x, self.y)
            return -1

        if not self.uncovered:
            self.flagged = True
            Paint.flagged(self.canvas, self.x, self.y)
            return 1
        return 0


class Grid:
    def __init__(self, *, width, height, n_mines):
        """
        Initalizes a Minesweeper board of size `width` * `height` with `n_mines`.
        Note that `n_mines` must be less than `width * height - 9`
        Params:
            width: the number of cells horizontally
            height: the number of cells vertically
            n_mines: the number of mines in the grid.
        """
        self.height = height
        self.width = width
        self.n_mines = min(n_mines, width * height - 9)

        # set up some GUI elements
        self.master = tk.Tk()
        self.timer = tk.Label(master=self.master, text="000.0")
        self.timer.grid(row=0)

        self.restart_button = tk.Button(
            text="Restart",
            background="#111111",
            activebackground="#333333",
            foreground="#EEEEEE",
            activeforeground="#FFFFFF",
            command=self.set_up,
        )
        self.restart_button.grid(row=0, column=1)

        self.mines_label = tk.Label(master=self.master, text=n_mines)
        self.mines_label.grid(row=0, column=2)

        self.canvas = tk.Canvas(master=self.master, width=width * CELL_WIDTH, height=height * CELL_WIDTH)
        self.canvas.grid(row=1, padx=CELL_WIDTH, pady=CELL_WIDTH, columnspan=3)
        self.canvas.bind("<Button-1>", lambda event: self.uncover_cell(event.x, event.y))
        self.canvas.bind("<Button-2>", lambda event: self.chord_cell(event.x, event.y))
        self.canvas.bind("<Button-3>", lambda event: self.flag_cell(event.x, event.y))

        self.set_up()
        self.master.mainloop()

    def update_timer(self):
        if self.first_click:
            self.timer.configure(text="000.0")
            return

        self.timer.configure(text=f"{(datetime.now() - self.start_time).total_seconds():05.1f}")
        self.master.after(100, self.update_timer)

    def set_up(self, free_x=None, free_y=None):
        """
        Configures the minefield, scattering the mines. If `free_x` and
        `free_y` are supplied, make sure that that position is empty by not
        placing a mine in it's neighbourhood.
        """
        self.flagged_mines = 0
        self.first_click = True

        self.cells = [[Cell(self.canvas, row=i, col=j) for i in range(self.width)] for j in range(self.height)]

        # set as mines
        mines_to_place = self.n_mines
        while mines_to_place > 0:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if free_x is not None and free_y is not None:
                if abs(x - free_x) <= 1 and abs(y - free_y) <= 1:
                    # skip if we're trying to place near/on the desired free spot
                    continue
            if self.cells[y][x].is_mine:
                continue
            self.cells[y][x].is_mine = True
            mines_to_place -= 1

        # determine neighbours
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if j > 0:
                    cell.add_neighbour(self.cells[i][j - 1])
                if j < len(row) - 1:
                    cell.add_neighbour(self.cells[i][j + 1])

                if i > 0:
                    cell.add_neighbour(self.cells[i - 1][j])
                    if j > 0:
                        cell.add_neighbour(self.cells[i - 1][j - 1])
                    if j < len(row) - 1:
                        cell.add_neighbour(self.cells[i - 1][j + 1])

                if i < len(self.cells) - 1:
                    cell.add_neighbour(self.cells[i + 1][j])
                    if j > 0:
                        cell.add_neighbour(self.cells[i + 1][j - 1])
                    if j < len(row) - 1:
                        cell.add_neighbour(self.cells[i + 1][j + 1])

                cell.update_count()

        self.start_time = datetime.now()

    def _get_cell_from_coord(self, x, y):
        """
        Returns the correct cell from the grid given pixel coordinates of the
        mouse click.
        """
        return self.cells[y // CELL_WIDTH][x // CELL_WIDTH]

    def uncover_cell(self, x, y):
        """
        Calls the proper cell's `uncover` function. If the cell is not an
        empty cell (i.e. it is a number or mine), reset the board and timer.
        Params:
            x: the x position of the click event
            y: the y position of the click event
        """
        cell = self._get_cell_from_coord(x, y)

        if self.first_click:
            state = cell.uncover()
            if state is not UncoverStatus.EMPTY:
                self.set_up(free_x=x // CELL_WIDTH, free_y=y // CELL_WIDTH)
            self.first_click = False
            self.update_timer()

        return self._get_cell_from_coord(x, y).uncover()

    def flag_cell(self, x, y):
        """
        Calls the proper cell's `flag` function and increments the grid's mine
        count.
        Params:
            x: the x position of the click event
            y: the y position of the click event
        """
        self.flagged_mines += self._get_cell_from_coord(x, y).flag()

        self.mines_label.configure(text=self.n_mines - self.flagged_mines)

    def chord_cell(self, x, y):
        """
        Calls the proper cell's `chord`
        Params:
            x: the x position of the click event
            y: the y position of the click event
        """
        self._get_cell_from_coord(x, y).chord()


if __name__ == "__main__":
    grid = Grid(height=16, width=30, n_mines=99)
