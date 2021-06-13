<script>
  import {ID} from "./storage";
  function auth(){
    localStorage.setItem("ID", "2e23:de42:de52:aw41");
    ID.set("2e23:de42:de52:aw41");
  }
</script>

<div class="main">
  <div class="authBox">
    <h1>Войти при помощи</h1>
    <button on:click={auth}>Sber Id</button>
    <div class="moreMethod">
      <img src="email.svg" on:click={auth}>
      <img src="github.svg" on:click={auth}>
      <img src="google.svg" on:click={auth}>
    </div>
  </div>
</div>

<style>
  .authBox{
    background-color: #343F48;
    border-radius: 8px;
    height: 200px;
    width: 300px;
    margin: auto;
    margin-top: calc(50% - 100px);
    display: flex;
    flex-direction: column;
  }
  h1{
    text-align: center;
    font-size: 24px;
    margin-top: 30px;
  }
  button{
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
  .moreMethod{
    display: flex;
    margin-top: auto;
    margin-bottom: 30px;
    justify-content: space-evenly;
  }
  img{
    width: 30px;
    height: 30px;
  }
</style>