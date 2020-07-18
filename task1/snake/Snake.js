class Snake {

    constructor(x, y) {
        const initCell = new Cell(Direction.LEFT, x, y);
        this.cells = [initCell];
    }

    getHead = () => this.cells[0];

    getLast = () => this.cells[this.cells.length - 1];

    setDirection = direction => this.getHead().direction = direction

    getDirection = () => this.getHead().direction;

    getAllCells = () => this.cells;

    isAllowedToMove = direction => oppositeDirection(this.getDirection()) !== direction;

    hasCollision = (cell) => {
        const hasCollision = this.cells.some(c => c.x === cell.x && c.y === cell.y);
        return hasCollision;
    }

    hasCollisionWithYourself = () => {
        const head = this.getHead();
        let hasCollision = false;
        for(let i = 1; i < this.cells.length - 1; i++) {
            if (head.x === this.cells[i].x && head.y === this.cells[i].y) {
                hasCollision = true;
            }
        } 
        return hasCollision;
    }

    draw = () => this.cells.forEach(cell => cell.draw());

    move(direction) {
        this.cells.forEach(cell => cell.move());
        for (let i = this.cells.length - 1; i > 0; i--) {
            this.cells[i].setDirection(this.cells[i - 1].direction)
        }
    }

}
