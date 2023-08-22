export default class GameActions {
    constructor() {
        this.top = -1
        this.actions = {}
    }

    get peek() {
        return this.actions[this.top];
    }

    push(value) {
        this.top += 1;
        this.actions[this.top] = value;
    }

    pop() {
        delete this.actions[this.top]
        this.top -= 1;
    }
}