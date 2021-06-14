import {get, writable} from 'svelte/store'
import {transport, ID} from "./storage";

export function deleteCookie(name) {
  setCookie(name, "", {
    'max-age': -1
  })
}

export function setToken(token) {
  setCookie("Bearer", token)
}

export function setCookie(name, value, options = {}) {
  options = {
    path: '/',
    ...options
  };
  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }
  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }
  document.cookie = updatedCookie;
}

export function storeFetch(url, method, data, token) {
  const store = writable(new Promise(() => {
  }));

  const setCache = (key, value) => {
    localStorage.setItem(key, JSON.stringify(value));
  }
  const getCache = (key) => {
    let saved = localStorage.getItem(key);
    return saved && JSON.parse(saved);
  }

  let cached = getCache(url)
  if (cached) {
    store.set(Promise.resolve(cached));
  }

  async function load() {

    let headers = {
      'Accept': 'application/json',
      "Content-Type": "application/json",
    }
    if (token) {
      headers['Authorization'] = 'Bearer ' + token;
    }

    let request = {
      method,
      // headers: new Headers(headers)
      headers
    };

    if (method !== 'GET') {
      request.body = JSON.stringify(data);
    }
    const response = await fetch(url, request);
    const rsp = await response.json();
    setCache(url, rsp);
    store.set(Promise.resolve(rsp));
  }

  load();
  return store;
}


// const apiUrl = 'https://b.sberchat.hackmasters.tech/'
export const apiUrl = 'http://localhost:8000/'
// const socketUrl = 'wss://b.sberchat.hackmasters.tech/'
export const socketUrl = 'ws://localhost:8000/'
export const fetches = {
  get: (apiPart, token = null) => {
    return storeFetch(new URL(apiPart, apiUrl), 'GET', {}, token)
  },
  post: (apiPart, data, token = null) => {
    return storeFetch(new URL(apiPart, apiUrl), 'POST', data, token)
  },
  delete: (apiPart, token = null) => {
    return storeFetch(new URL(apiPart, apiUrl), 'DELETE', {}, token)
  },
}

export function connect() {
  let socket = new WebSocket(socketUrl + "chats/" + get(ID));
  console.log(socket)
  socket.onopen = function () {
    console.log("Соединение установлено.");
  };

  socket.onclose = function (event) {
    if (event.wasClean) {
      console.log('Соединение закрыто чисто');
    } else {
      console.log('Обрыв соединения'); // например, "убит" процесс сервера
    }
    console.log('Код: ' + event.code + ' причина: ' + event.reason);
  };

  socket.onmessage = function (event) {
    console.log("Получены данные " + event.data);
    transport.data.set(event.data);
  };
  transport.channel = socket;
}