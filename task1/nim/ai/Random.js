class Random {
    constructor(game) {
        this.game = game;
    }

    nextMove = () => Math.floor(Math.random() * this.game.getRemoveMax()) + 1;
}
