import random
# from tkinter import Tk, Label, Button

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

class Cell:
    def __init__(self):
        self.is_mine = False
        self.uncovered = False
        self.neighbours = []
        self.highlight = False
        self.flagged = False

    def update_count(self):
        self.count = sum(cell.is_mine for cell in self.neighbours)

    def add_neighbour(self, cell):
        self.neighbours.append(cell)

    def uncover(self):
        '''
        Returns True if success, False if blows up
        '''
        if self.uncovered:
            return True

        self.uncovered = True
        self.highlight = True
        if self.count == 0:
            for neighbour in self.neighbours:
                neighbour.uncover()
            return True

        if self.is_mine:
            return False
        return True

    def flag(self):
        if not self.uncovered:
            self.flagged = True

    def __repr__(self):
        if self.flagged:
            return "\033[1;31m!\033[1;m"
        if not self.uncovered:
            return "\033[1;40m \033[1;m"
        if self.is_mine:
            if self.highlight:
                self.highlight = False
                return "\033[91m\033[1m{}\033[0m".format("@")  # bold red @
            return "@"
        if self.count:
            if self.highlight:
                self.highlight = False
                return "\033[1;47m\033[1;34m{}\033[0m".format(self.count)
            return "\033[1;47m\033[1;35m{}\033[0m".format(self.count)
        return "\033[1;47m \033[1;m"


class Grid:
    def __init__(self, *, width, height, n_mines):
        self.height = height
        self.width = width
        self.n_mines = n_mines

        self.cells = [[Cell() for i in range(self.width)] for j in range(self.height)]

        # set as mines
        mines_to_place = n_mines
        while mines_to_place > 0:
            self.cells[random.randrange(self.height)][random.randrange(self.width)].is_mine = True
            mines_to_place -= 1

        # determine neighbours
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if j > 0: cell.add_neighbour(self.cells[i][j - 1])
                if j < len(row) - 1: cell.add_neighbour(self.cells[i][j + 1])

                if i > 0:
                    cell.add_neighbour(self.cells[i - 1][j])
                    if j > 0: cell.add_neighbour(self.cells[i - 1][j - 1])
                    if j < len(row) - 1: cell.add_neighbour(self.cells[i - 1][j + 1])

                if i < len(self.cells) - 1:
                    cell.add_neighbour(self.cells[i + 1][j])
                    if j > 0: cell.add_neighbour(self.cells[i + 1][j - 1])
                    if j < len(row) - 1: cell.add_neighbour(self.cells[i + 1][j + 1])

                cell.update_count()

    def __repr__(self):
        repr_str = "   " + "".join(alphabet[i] for i in range(self.width)) + "\n"
        repr_str += "  " + "⎽" * (2 + self.width) + "\n"
        for i, row in enumerate(self.cells, 1):
            repr_str += "{}|".format(str(i).rjust(2))
            for cell in row:
                repr_str += str(cell)
            repr_str += "|\n"
        return repr_str + "  " + ("⎺" * (2 + self.width))

    def _convert_coordinate(self, coordinate):
        pos_x = alphabet.index(coordinate[0])
        pos_y = int(coordinate[1:]) - 1

        if pos_x >= len(self.cells[0]): pos_x = None
        if pos_y >= len(self.cells): pos_y = None

        return pos_x, pos_y

    def uncover_cell(self, coordinate):
        pos_x, pos_y = self._convert_coordinate(coordinate)
        if pos_x is None or pos_y is None: return True

        if self.cells[pos_y][pos_x].uncover():
            print(self)
            return True

        print(self)
        print("YOU BLEW UP!")
        return False

    def flag_cell(self, coordinate):
        pos_x, pos_y = self._convert_coordinate(coordinate)
        if pos_x is None or pos_y is None: return

        self.cells[pos_y][pos_x].flag()
        print(self)


if __name__ == "__main__":
    grid = Grid(height=16, width=30, n_mines=99)

    print(grid)

    while(True):
        print("Enter a command: ")
        print("'Flag A4' or 'Reveal c15'")
        command, coordinate = input("").split(" ")
        if command in ["Flag", "F", "f", "flag"]:
            grid.flag_cell(coordinate)
        if command in ["Reveal", "R", "r", "reveal"]:
            grid.uncover_cell(coordinate)
