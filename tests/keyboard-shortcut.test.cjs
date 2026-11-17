const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const html = fs.readFileSync(path.join(__dirname, '../templates/index.html'), 'utf8');
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n');

function press(overrides = {}, value = '  hello  ') {
    const emissions = [];
    let handler;
    const input = { value, addEventListener(name, callback) {
        assert.equal(name, 'keydown');
        handler = callback;
    } };
    vm.runInNewContext(script, {
        io: () => ({ on() {}, emit: (...args) => emissions.push(args) }),
        document: { getElementById(id) { assert.equal(id, 'memo-input'); return input; } },
    });
    const event = { key: 'Enter', metaKey: false, ctrlKey: false, isComposing: false,
        defaultPrevented: false, preventDefault() { this.defaultPrevented = true; }, ...overrides };
    handler(event);
    return { emissions, event, input };
}

for (const [name, keys] of [['Ctrl+Enter', {ctrlKey: true}], ['Cmd+Enter', {metaKey: true}], ['both modifiers', {ctrlKey: true, metaKey: true}]]) {
    test(`${name} saves once and prevents an extra newline`, () => {
        const r = press(keys);
        assert.equal(r.emissions.length, 1);
        assert.equal(r.emissions[0][0], 'add_memo');
        assert.equal(r.emissions[0][1].content, 'hello');
        assert.equal(r.input.value, '');
        assert.equal(r.event.defaultPrevented, true);
    });
}
for (const [name, keys] of [['plain Enter', {}], ['other key', {key: 'a', ctrlKey: true}], ['IME composition', {isComposing: true, metaKey: true}]]) {
    test(`${name} does not save or prevent normal input`, () => {
        const r = press(keys);
        assert.equal(r.emissions.length, 0);
        assert.equal(r.input.value, '  hello  ');
        assert.equal(r.event.defaultPrevented, false);
    });
}
test('empty shortcut input does not emit a memo', () => {
    const r = press({ctrlKey: true}, '   ');
    assert.equal(r.emissions.length, 0);
});
