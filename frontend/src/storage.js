import { writable } from 'svelte/store';

function createCount() {
  const { subscribe, set, update } = writable(1);

  return {
    subscribe,
    increment: () => update(n => n + 1),
    decrement: () => update(n => n - 1),
    reset: () => set(0)
  };
}

export const settingWindowState = createCount();