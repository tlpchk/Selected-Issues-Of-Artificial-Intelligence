class NodeState {
    #nim;
    #label;
    #winCount;
    #visitCount;

    constructor(player, N, removeMax, label = 0) {
        this.#nim = new Nim(N, player, removeMax);
        this.#label = label;
        this.#winCount = 0;
        this.#visitCount = 0;
    }

    getNim = () => this.#nim;

    getLabel = () => this.#label;

    getWinCount = () => this.#winCount;

    getVisitCount = () => this.#visitCount;

    incrementVisitCount = () => this.#visitCount += 1;

    incrementWinCount = () => this.#winCount += 1;

    createChildState = (label) => {
        return new NodeState(this.#nim.getNextPlayer(), this.#nim.getN() - label, this.#nim.getRemoveMax(), label);
    };

    toString = () => {
        return this.#label.toString() + " " + this.#winCount.toString() + "/" + this.#visitCount.toString()}
}