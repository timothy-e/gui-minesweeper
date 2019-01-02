"use strict";
exports.__esModule = true;
var Cell = (function () {
    function Cell() {
        this.is_mine = false;
        this.revealed = false;
        this.highlighted = false;
        this.flagged = false;
        this.count = 0;
    }
    Cell.prototype.update_count = function () {
        var _this = this;
        this.neighbours.forEach(function (neighbour) {
            if (neighbour.is_mine) {
                _this.count++;
            }
        });
    };
    Cell.prototype.add_neighbour = function (cell) {
        this.neighbours.push(cell);
    };
    Cell.prototype.uncover = function () {
        if (this.revealed)
            return true;
        this.revealed = true;
        this.highlighted = true;
        if (this.count == 0) {
            this.neighbours.forEach(function (neighbour) {
                neighbour.uncover();
            });
        }
        if (this.is_mine)
            return false;
        return true;
    };
    Cell.prototype.flag = function () {
        if (!this.revealed)
            this.flagged = true;
    };
    Cell.prototype.display = function () {
        if (this.flagged)
            return "!";
        if (!this.revealed)
            return "?";
        if (this.is_mine) {
            if (this.highlighted) {
                this.highlighted = false;
                return "@";
            }
            return "@";
        }
        if (this.count > 0) {
            if (this.highlighted) {
                this.highlighted = false;
                return this.count.toString();
            }
            return this.count.toString();
        }
    };
    return Cell;
}());
var Grid = (function () {
    function Grid(width, height, n_mines) {
        this.width = width;
        this.height = height;
        this.n_mines = n_mines;
        this.cells = [];
        var i;
        for (i = 0; i < height; i++) {
            var cell_row = [];
            var j;
            for (j = 0; j < width; j++) {
                cell_row.push(new Cell());
            }
            this.cells.push(cell_row);
        }
        while (n_mines > 0) {
            this.cells[Math.floor(Math.random() * this.height)][Math.floor(Math.random() * this.width)].is_mine = true;
            n_mines -= 1;
        }
        for (i = 0; i < height; i++) {
            var j;
            for (j = 0; j < width; j++) {
                if (j > 0)
                    this.cells[i][j].add_neighbour(this.cells[i][j - 1]);
                if (j < width - 1)
                    this.cells[i][j].add_neighbour(this.cells[i][j + 1]);
                if (i > 0) {
                    this.cells[i][j].add_neighbour(this.cells[i - 1][j]);
                    if (j > 0)
                        this.cells[i][j].add_neighbour(this.cells[i - 1][j - 1]);
                    if (j < width - 1)
                        this.cells[i][j].add_neighbour(this.cells[i - 1][j + 1]);
                }
                if (i < height - 1) {
                    this.cells[i][j].add_neighbour(this.cells[i + 1][j]);
                    if (j > 0)
                        this.cells[i][j].add_neighbour(this.cells[i + 1][j - 1]);
                    if (j < width - 1)
                        this.cells[i][j].add_neighbour(this.cells[i + 1][j + 1]);
                }
            }
            this.cells[i][j].update_count();
        }
    }
    Grid.prototype.display = function () {
        this.cells.forEach(function (row) {
            row.forEach(function (cell) {
                console.log(cell.display());
            });
            console.log("\n");
        });
    };
    return Grid;
}());
function init() {
    var grid = new Grid(16, 30, 99);
    return 0;
}
init();
//# sourceMappingURL=minesweeper.js.map