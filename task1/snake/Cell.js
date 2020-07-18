class Cell {
    WIDTH = 20;

    constructor(direction = Direction.NONE,
                x = this.getRandomValue(),
                y = this.getRandomValue()) {
        this.x = x;
        this.y = y;
        this.direction = direction;
    }

    getRandomValue = () => Math.ceil(Math.random() * this.WIDTH - 1);

    draw() {
        rect(
            this.x * this.WIDTH,
            this.y * this.WIDTH,
            this.WIDTH,
            this.WIDTH
        );
    }

    move() {
        switch (this.direction) {
            case Direction.LEFT:
                this.x = this.x - 1;
                break;
            case Direction.RIGHT:
                this.x += 1;
                break;
            case Direction.UP:
                this.y -= 1;
                break;
            case Direction.DOWN:
                this.y += 1;
                break;
        }
    }

    setDirection(newDirection) {
        this.direction = newDirection;
    }
}