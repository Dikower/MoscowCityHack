<script>
  import {ID, transport, contacts} from "./storage";
  import {fetches, setCookie, setToken, connect} from "./api";
  import {get} from 'svelte/store'

  let email = 'eeli.palo@example.com';

  async function auth() {
    let data = await get(fetches.post('/users/login', {
      "login_method": "email", "email": email, "fio": "Дмитрий Дин", "avatar":
        "https://randomuser.me/api/portraits/men/68.jpg"
    }))
    data = await get(fetches.post("/users/auth", {token: data.token}));
    let token = data.token;
    localStorage.setItem("ID", token);
    ID.set(token);
    contacts.set(await get(fetches.get('/chats/my', token)))
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
    <input bind:value={email}>

  </div>
</div>

<style>
  .authBox {
    background-color: #343F48;
    border-radius: 8px;
    height: 250px;
    width: 300px;
    margin: auto;
    margin-top: calc(50% - 100px);
    display: flex;
    flex-direction: column;
  }

  input {
    width: 80%;
    margin: 0 auto;
    margin-bottom: 20px;
    text-align: center;
    border-radius: 10px;
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