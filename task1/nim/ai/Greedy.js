class Greedy {
    constructor(game) {
        this.game = game;
    }

    nextMove = () => {
        let choice = game.getN() % (game.getRemoveMax() + 1);
        if (choice === 0) {
            choice = 1
        }
        return choice
    }
}
