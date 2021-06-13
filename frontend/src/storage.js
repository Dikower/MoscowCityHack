import { writable } from 'svelte/store';

function createCount() {
  const { subscribe, set, update } = writable(0);

  return {
    subscribe,
    increment: () => update(n => n + 1),
    decrement: () => update(n => n - 1),
    reset: () => set(0)
  };
}

export const ID = writable("");

export const settingWindowState = createCount();
export const groupWindowState = createCount();
export const channelWindowState = createCount();
export const contactsWindowState = createCount();