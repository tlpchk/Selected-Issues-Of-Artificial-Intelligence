class Node {
    #state;
    #parent;
    #children;

    constructor(state, parent = undefined) {
        this.#state = state;
        this.#parent = parent;
        this.#children = []
    }

    isAllChildrenVisited(){
        return this.#children.length === this.#state.getNim().getRemoveMax()
    }

    getUnexploredLabels() {
        let explored = this.#children.map(child => child.getState().getLabel());
        let unexplored = [];
        for (let i=1; i<= this.#state.getNim().getRemoveMax(); i++){
            if(!explored.includes(i)){
                unexplored.push(i)
            }
        }
        return unexplored;
    }

    addChild = (child) => this.#children.push(child);

    getState = () => this.#state;

    getChildren = () => this.#children;

    getParent = () => this.#parent;

    setParent = (parent) => this.#parent = parent

    isLeaf = () => this.#children.length === 0
}