<script>
  import { settingWindowState } from './storage.js';
  function closeWindow(){
    settingWindowState.decrement();
  }
</script>

<div class="WindowBox">
  <div class="BoxForSetting">

  </div>
  <h1>modal window</h1>
  <button on:click={closeWindow}>exit</button>
</div>

<style>
  .WindowBox{
    position: absolute;
    /*background-color: #999999;*/
    height: 100%;
    width: 100%;
  }
</style>