import {describe, expect, it, beforeEach} from '@jest/globals';
import GameActions from "..//utils/GameActions.js";

describe('Game Actions', () => {

    let stack;

    beforeEach(() => {
        stack = new GameActions();
    });

    it('it created empty', function () {
        expect(stack.top).toBe(0);
        expect(stack.actions).toEqual({});
    });

    it('can push to the top', () => {
        stack.push('❤️')
        expect(stack.top).toBe(1);
        expect(stack.peek).toBe('❤️')
    });

    it('can pop off', () => {
        stack.push('❤️')
        stack.push('✅')
        expect(stack.top).toBe(2)
        expect(stack.peek).toBe('✅')
        stack.pop()
        expect(stack.top).toBe(1)
        expect(stack.peek).toBe('❤️')
    });
})