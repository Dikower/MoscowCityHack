import {writable} from 'svelte/store'

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
    }
    if (token) {
      headers['Authorization'] = 'Bearer ' + token;
    }

    let request = {
      method,
      // headers: new Headers(headers)
      headers
    };

    if (method !== 'get') {
      request.body = JSON.stringify(data)
    }
    console.log(request)
    const response = await fetch(url, request);
    const rsp = await response.json();
    setCache(url, rsp);
    store.set(Promise.resolve(rsp));
  }

  load();
  return store;
}


const apiUrl = 'https://b.sberchat.hackmasters.tech/'
// const apiUrl = 'http://localhost:8000/'
export const fetches = {
  get: (apiPart, token = null) => {
    return storeFetch(new URL(apiPart, apiUrl), 'get', {}, token)
  },
  post: (apiPart, data, token = null) => {
    return storeFetch(new URL(apiPart, apiUrl), 'post', data, token)
  },
  delete: (apiPart, token = null) => {
    return storeFetch(new URL(apiPart, apiUrl), 'delete', {}, token)
  },
}