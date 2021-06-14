<script>
  import {ID, transport} from "./storage";
  import {fetches, setCookie, socketUrl, setToken, connect} from "./api";
  import {get} from 'svelte/store'

  async function auth() {
    let data = await get(fetches.post('/users/login', {
      "login_method": "email", "email": "eemil.peltola@example.com"
    }))
    let token = await get(fetches.post("/users/auth", {token: data.token}));
    localStorage.setItem("ID", token);
    ID.set(token);
    connect();
  }

  async function email_auth() {
    auth();
  }

</script>

<div class="main">
  <div class="authBox">
    <h1>Войти при помощи</h1>
    <button on:click={auth}>Sber Id</button>
    <div class="moreMethod">
      <img src="email.svg" alt="email-icon" on:click={email_auth}>
      <img src="github.svg" alt="github-icon" on:click={auth}>
      <img src="google.svg" alt="google-icon" on:click={auth}>
    </div>
  </div>
</div>

<style>
  .authBox {
    background-color: #343F48;
    border-radius: 8px;
    height: 200px;
    width: 300px;
    margin: auto;
    margin-top: calc(50% - 100px);
    display: flex;
    flex-direction: column;
  }

  h1 {
    text-align: center;
    font-size: 24px;
    margin-top: 30px;
  }

  button {
    background: #1AA291;
    border: none;
    border-radius: 24px;
    color: white;
    width: 60%;
    margin-left: auto;
    margin-right: auto;
    /*margin-top: auto;*/
    margin-bottom: -15px;
  }

  .moreMethod {
    display: flex;
    margin-top: auto;
    margin-bottom: 30px;
    justify-content: space-evenly;
  }

  img {
    width: 30px;
    height: 30px;
  }
</style>