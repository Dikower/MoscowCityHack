<script>
  import { settingWindowState } from '../storage.js';
  let checkMat = false;
  let checkToxic = false;
  let checkPrInfo = false;
  let changeState = false;

  let userData = {name: "Димочка", img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"}
  let name = userData.name;
  function closeWindow(){
    settingWindowState.decrement();
  }
  function saveSettings(){
    alert("Saving...")
  }
  function changeName(){
    changeState = !changeState;
  }
  function saveName(){
    userData.name = name;
    changeState = !changeState;
  }
</script>

<div class="WindowBox">
  <div class="BoxForSetting">
    <button on:click={closeWindow} class="cancel-button">
      <img src="cancel.svg" class="cancel-icon" alt="cancel-icon" />
    </button>
    <div class="userInfo">
      <img src={userData.img}>
      {#if !changeState}
        <div class="user-name">
        <h1>{userData.name}</h1>
          <button on:click={changeName} class="edit-button">
            <img src="edit.svg" class="edit-icon" alt="edit-icon" />
          </button>
        </div>
      {:else}
        <input bind:value={name}>
        <button on:click={saveName}>Сохранить</button>
      {/if}

    </div>

    <div class="oneSettingBox">
      <h3>Скрытие матов</h3>
      <label class="switch">
        <input type="checkbox" checked={checkMat}>
        <span class="slider round"></span>
      </label>
    </div>
    <div class="oneSettingBox">
      <h3>Проверка на токсичность</h3>
      <label class="switch">
        <input type="checkbox" checked={checkToxic}>
        <span class="slider round"></span>
      </label>
    </div>
    <div class="oneSettingBox">
      <h3>Проверка на приватную информацию</h3>
      <label class="switch">
        <input type="checkbox" checked={checkPrInfo}>
        <span class="slider round"></span>
      </label>
    </div>
    <button on:click={closeWindow}>exit</button>
    <button on:click={saveSettings}>save</button>
  </div>

</div>

<style>
  h1, h4 {
    color: #fff;
  }

  .edit-icon {
    height: 16px;
    width: 16px;
  }

  .user-name {
    display: flex;
  }

  .edit-button {
    background-color: transparent;
    border: none;
    outline: none;
  }

  .cancel-button {
    display: flex;
    align-items: center;
    justify-content: center;
    align-self: flex-end;
    width: auto;
    height: 16px;
    padding: 0;
    border: none;
    outline: none;
    background-color: transparent;
}

  .userInfo h1{
    margin-top: auto;
    margin-bottom: auto;
    margin-left: 10px;
  }
  .userInfo input{
    height: 30px;
    width: 100px;
    margin-top: auto;
    margin-bottom: auto;
  }
  .userInfo button{
    height: 50px;
    margin-top: auto;
    margin-bottom: auto;
    margin-left: auto;
  }
  img{
    height: 100px;
    width: 100px;
    border-radius: 100px;
  }
  .WindowBox{
    position: absolute;
    height: 100%;
    width: 100%;
  }

  .switch {
    margin-top: 0;
    line-height: 0;
  }

  h4 {
    margin-bottom: 5px;
  }

  .oneSettingBox {
    display: flex;
    flex-direction: column;
  }

  .cancel-icon {
    width: 16px;
  }
  .BoxForSetting{
    padding: 20px;
    border-radius: 10px;
    background-color: #343F48;
    margin-left: 6%;
    height: auto;
    width: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
  }
</style>
