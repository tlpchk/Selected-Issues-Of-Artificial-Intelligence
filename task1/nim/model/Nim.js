class Nim {
    #N;
    #currentPlayer;
    #removeMax;
    #withCoin;

    constructor(N, currentPlayer, removeMax, withCoin = false) {
        this.#N = N;
        this.#currentPlayer = currentPlayer;
        this.#removeMax = removeMax;
        this.#withCoin = withCoin;
    }

    over() {
        return this.#N <= 0
    };

    randomPlay() {
        let randomChoice = 1 + Math.floor(Math.random() * this.#removeMax);
        this.decreaseN(randomChoice)
    }

    getN() {
        return this.#N;
    }

    tossCoin = () => {
        return Math.floor(Math.random() * 2);
    };


    decreaseN(n) {
        this.#N -= n;
        if (this.#withCoin) {
            this.#N -= this.tossCoin()
        }
    }

    getNextPlayer() {
        return 3 - this.#currentPlayer
    }

    switchPlayer = () => {
        this.#currentPlayer = this.getNextPlayer()
    };

    getCurrentPlayer = () => this.#currentPlayer;

    getRemoveMax() {
        return this.#removeMax
    }

    getPlayer = () => this.#currentPlayer;

    copy() {
        return new Nim(this.#N, this.#currentPlayer, this.#removeMax)
    }
}
