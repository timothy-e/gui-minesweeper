import { inherits } from "util";

class Cell {
    neighbours: Array<Cell>;
    is_mine: boolean;
    revealed: boolean;
    highlighted: boolean;
    flagged: boolean;
    count: number;

    constructor() {
        this.is_mine = false
        this.revealed = false
        this.highlighted = false
        this.flagged = false
        this.count = 0
    }

    update_count() {
        this.neighbours.forEach(neighbour => {
            if (neighbour.is_mine) {
                this.count ++
            }
        })
    }

    add_neighbour(cell: Cell) {
        this.neighbours.push(cell)
    }

    uncover() {
        if (this.revealed) return true
        this.revealed = true
        this.highlighted = true

        if (this.count == 0) {
            this.neighbours.forEach(neighbour => {
                neighbour.uncover()
            });
        }

        if (this.is_mine) return false
        return true
    }

    flag() {
        if (!this.revealed) this.flagged = true
    }

    display() {
        if (this.flagged) return "!"
        if (!this.revealed) return "?"
        if (this.is_mine) {
            if (this.highlighted) {
                this.highlighted = false
                return "@"
            }
            return "@"
        }
        if (this.count > 0) {
            if (this.highlighted) {
                this.highlighted = false
                return this.count.toString()
            }
            return this.count.toString()
        }
    }
}

class Grid {
    height: number;
    width: number;
    n_mines: number;
    cells: Array<Array<Cell>>
    constructor(width: number, height: number, n_mines: number) {
        this.width = width;
        this.height = height;
        this.n_mines = n_mines;

        this.cells = [];
        var i: number;
        for (i = 0; i < height; i ++) {
            var cell_row: Array<Cell> = [];
            var j: number;
            for (j = 0; j < width; j ++) {
                cell_row.push(new Cell());
            }
            this.cells.push(cell_row);
        }

        // Add mines
        while (n_mines > 0) {
            this.cells[Math.floor(Math.random() * this.height)][Math.floor(Math.random() * this.width)].is_mine = true;
            n_mines -= 1;
        }

        // Determine neighbours
        for (i = 0; i < height; i++) {
            var j: number;
            for (j = 0; j < width; j++) {
                if (j > 0) this.cells[i][j].add_neighbour(this.cells[i][j - 1])
                if (j < width - 1) this.cells[i][j].add_neighbour(this.cells[i][j + 1])

                if (i > 0) {
                    this.cells[i][j].add_neighbour(this.cells[i - 1][j])
                    if (j > 0) this.cells[i][j].add_neighbour(this.cells[i - 1][j - 1])
                    if (j < width - 1) this.cells[i][j].add_neighbour(this.cells[i - 1][j + 1])
                }

                if (i < height - 1) {
                    this.cells[i][j].add_neighbour(this.cells[i + 1][j])
                    if (j > 0) this.cells[i][j].add_neighbour(this.cells[i + 1][j - 1])
                    if (j < width - 1) this.cells[i][j].add_neighbour(this.cells[i + 1][j + 1])
                }
            }
            this.cells[i][j].update_count()
        }
    }

    display() {
        this.cells.forEach(row => {
            row.forEach(cell => {
                console.log(cell.display());
            })
            console.log("\n");
        })
    }
}

function init() {
    var grid = new Grid(16, 30, 99);
    return 0;
}

init();
