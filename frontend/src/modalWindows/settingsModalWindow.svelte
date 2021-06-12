<script>
  import { settingWindowState } from '../storage.js';
  let checkMat = false;
  let checkToxic = false;
  let checkPrInfo = false;
  function closeWindow(){
    settingWindowState.decrement();
  }
  function saveSettings(){
    alert("Saving...")
  }
</script>

<div class="WindowBox">
  <div class="BoxForSetting">
    <h1>settings</h1>
    <div class="oneSettingBox">
      <h4>Скрытие матов - </h4>
      <input type=checkbox class="checkbox" checked={checkMat}>
    </div>
    <div class="oneSettingBox">
      <h4>Проверка на токсичность - </h4>
      <input type=checkbox class="checkbox" checked={checkToxic}>
    </div>
    <div class="oneSettingBox">
      <h4>Проверка на приватную информацию - </h4>
      <input type=checkbox class="checkbox" checked={checkPrInfo}>
    </div>
    <button on:click={closeWindow}>exit</button>
    <button on:click={saveSettings}>save</button>
  </div>

</div>

<style>
  .WindowBox{
    position: absolute;
    height: 100%;
    width: 100%;
  }
  .BoxForSetting{
    background-color: whitesmoke;
    margin-top: 6%;
    margin-left: 6%;
    height: 500px;
    width: 300px;
  }
  .oneSettingBox{
    display: flex;
  }
  .checkbox{
    margin-top: auto;
    margin-bottom: auto;
    margin-left: 10px;
  }
</style>
