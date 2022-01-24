<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import { computed, reactive, Ref, ref } from 'vue';
import words from './assets/words.json';

type State = 'green' | 'yellow' | 'grey';

const alphaNumbers = Array.from(Array(26)).map((e, i) => i + 65);
const alphabets = alphaNumbers
  .map((x) => String.fromCharCode(x));
const lookup = reactive(alphabets
  .reduce((map, a: string) => {
    map[a] = { state: 'grey', index: -1 };
    return map;
  }, {} as { [key: string]: { state: State, index: number; }; }));
const guesses: Ref<string[]> = ref([]);
const input = ref('');

let stats = {};
for (let word of words) {
  let uniqueChar = [...new Set(word.split(''))];
}

let possibleWords = computed(() => {
  let positions = [];
  let wrongPosition: string[] = [];
  for (let i = 0; i < 5; i++) {
    positions[i] = `[${alphabets.join('')}]`;
  }

  for (let [char, { state, index }] of Object.entries(lookup)) {
    if (index === -1) continue;
    if (state === 'green') {
      positions[index] = `[${char}]`;
    } else if (state === 'yellow') {
      wrongPosition.push(char);
      positions[index] = positions[index].replace(char, '');
    } else if (state === 'grey') {
      for (let i = 0; i < 5; i++) {
        positions[i] = positions[i].replace(char, '');
      }
    }
  }
  let regex = new RegExp(positions.join(''));
  return words
    .filter(w => regex.test(w.toUpperCase()))
    .filter(w => wrongPosition.every(yellow => w.toUpperCase().includes(yellow)))
    .sort((a, b) => a.localeCompare(b));
});

function submit() {
  if (!input.value) return;
  let value = input.value.toUpperCase();
  guesses.value.push(value);
  guesses.value.forEach(g => g.split('').forEach((char, i) => {
    if (lookup[char].index === -1) {
      lookup[char].index = i;
    }
  }));
  input.value = '';
}

function remove(guess: string) {
  for (let char of guess.split('')) {
    // Check if safe to lookup for char
    if (guesses.value.every(g => g === guess || (g !== guess && !g.split('').includes(char)))) {
      lookup[char].state = 'grey';
      lookup[char].index = -1;
    }
  }
  guesses.value = guesses.value.filter(g => g !== guess);
}

function change(char: string, index: number) {
  lookup[char].index = index;
  switch (lookup[char].state) {
    case 'grey':
      lookup[char].state = 'yellow';
      break;
    case 'yellow':
      lookup[char].state = 'green';
      break;
    case 'green':
      lookup[char].state = 'grey';
      break;
    default:
      console.log('Error', lookup[char].state);
      break;
  }
}
</script>

<template>
  <div style="font-size: 24px; display: flex; justify-content: center;">
    <div v-for="char in 'wordle'.split('')" class="char">{{ char.toUpperCase() }}</div>
  </div>
  <div style="margin-top: 20px; margin-bottom: 50px; text-align: center;">
    <div>Make guesses in the input box</div>
    <div>Click on the characters in the guesses to change the color</div>
  </div>

  <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
    <div v-for="guess in guesses" style="display: flex; justify-content: center; width: 100%;">
      <div
        v-for="(char, i) in guess.split('')"
        @click="change(char, i)"
        :class="['char', lookup[char].index === i ? lookup[char].state : '']"
      >{{ char }}</div>

      <button @click="remove(guess)">Remove</button>
    </div>
  </div>
  <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
  <!-- <HelloWorld msg="Hello Vue 3 + TypeScript + Vite" /> -->

  <div>Possible words ({{ possibleWords.length }})</div>
  <div class="list-container">
    <div v-for="word in possibleWords.slice(0, 100)">{{ word.toUpperCase() }}</div>
    <div v-if="possibleWords.length > 100">...</div>
  </div>

  <div style="display: flex; flex-direction: column;">
    <input v-model="input" @keyup.enter="submit()" class="input-field" />
    <button class="btn" @click="submit()">GUESS</button>
  </div>
</template>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}
body {
  /* background-color: #1a1a1a; */
  background-color: #2c3e50;
  color: #cfd8dc;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  padding-top: 20px;
}

.btn {
  appearance: button;
  background-color: #1899D6;
  border: solid transparent;
  border-radius: 5px;
  border-width: 0 0 4px;
  box-sizing: border-box;
  color: #FFFFFF;
  cursor: pointer;
  display: inline-block;
  font-family: din-round,sans-serif;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: .8px;
  line-height: 20px;
  outline: none;
  overflow: visible;
  padding: 13px 16px;
  text-align: center;
  text-transform: uppercase;
  touch-action: manipulation;
  transform: translateZ(0);
  transition: filter .2s;
  user-select: none;
  -webkit-user-select: none;
  vertical-align: middle;
  white-space: nowrap;
  width: 170px;
	margin: 0 auto;
}

.btn:after {
  background-clip: padding-box;
  background-color: #1CB0F6;
  border: solid transparent;
  border-radius: 5px;
  border-width: 0 0 4px;
  bottom: -4px;
  content: "";
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
  z-index: -1;
}

.btn:main,
.btn:focus {
  user-select: auto;
}

.btn:hover:not(:disabled) {
  filter: brightness(1.1);
}

.btn:disabled {
  cursor: auto;
}

.btn:active {
  transition: .25s;
  transform: scale(0.9);
}

.list-container {
  font-family: monospace;
  font-size: 14px;
  margin-left: auto;
  margin-right: auto;
  padding: 10px;
  margin-bottom: 20px;
  height: 200px;
  width: 150px;
  overflow-y: scroll;
  box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}

.list-container > div {
  margin-bottom: 6px;
}

.char {
  font-size: 16px;
  font-weight: bold;
  width: 50px;
  height: 50px;
  border: 1px solid lightgrey;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  background-color: #939598;
}

.grey {
  background-color: #939598;
}

.yellow {
  background-color: #b59f3b;
}

.green {
  background-color: #538d4e;
}

.input-field {
  color: #333;
  font-size: 1.2rem;
  width: 150px;
  height: 30px;
	margin: 0 auto;
  margin-bottom: 10px;
  padding: 0.5rem 0.5rem;
  border-radius: 0.2rem;
  background-color: rgb(255, 255, 255);
}
</style>
