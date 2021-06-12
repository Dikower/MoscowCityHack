<script>
  import {channelWindowState} from '../storage.js';
  import {fetches} from "../api";

  let errorMessage = "";
  let channelName = "";
  let stateWindow = true;
  let peoplemass = fetches.get('/users/all'); //TODO
  let newPeopleMass = [];
  $: if ($peoplemass instanceof Promise) $peoplemass.then(v => {$peoplemass = v; newPeopleMass = $peoplemass;})

  function closeWindow() {
    channelWindowState.decrement();
  }

  function nextStep() {
    if (channelName === "") {
      errorMessage = "Введите название группы!";
      return;
    }
    stateWindow = !stateWindow;
  }

  function prevStep() {
    stateWindow = !stateWindow;
  }

  function createFunc() {
    //тут запрос с добавлением чата
    closeWindow();
  }

  function searchContact(event) {
    let reqName = event.target.value;
    if (reqName === "") {
      newPeopleMass = $peoplemass;
    } else {
      newPeopleMass = [];
      $peoplemass.forEach(element => {
        let elName = element.name.toLowerCase();
        if (elName.indexOf(reqName.toLowerCase()) !== -1) {
          newPeopleMass = newPeopleMass.concat(element);
        }
      });
    }
  }
</script>

<div class="WindowBox">
  {#if stateWindow}
    <div class="mainBox">
      <h3>Channel name</h3>
      <input bind:value={channelName}>
      {#if errorMessage !== ""}
        <h5>{errorMessage}</h5>
      {/if}
      <div class="buttons">
        <button on:click={nextStep}>next</button>
        <button on:click={closeWindow}>exit</button>
      </div>
    </div>
  {:else}
    <div class="mainBoxSecond">
      <h3>Add Members to {channelName}</h3>
      <input on:input={searchContact}>
      <div class="peopleColumn">
        <div class="scrollable">
          {#await $peoplemass}
            {:then data}
              {#each newPeopleMass as man}
                <div class="manBox">
                  <img src={man.img} alt="">
                  <h4>{man.name}</h4>
                </div>
              {/each}
          {/await}
        </div>
      </div>
      <div class="buttonsBox">
        <button on:click={prevStep}>cancel</button>
        <button on:click={createFunc}>create</button>
      </div>
    </div>
  {/if}
</div>

<style>
  .WindowBox {
    position: absolute;
    /*background-color: #999999;*/
    /*opacity: 0.7;*/
    height: 100%;
    width: 100%;
    /*z-index:3;*/
  }

  .mainBox {
    background-color: whitesmoke;
    width: 300px;
    /*margin-top: calc(50% - 60px);*/
    /*margin-left: calc(50% - 150px);*/
    margin-top: 10%;
    margin-left: 6%;
    display: flex;
    flex-direction: column;
  }

  .mainBoxSecond {
    background-color: whitesmoke;
    width: 300px;
    height: 450px;
    /*margin-top: 20%;*/
    /*margin-left: calc(50% - 150px);*/
    margin-top: 10%;
    margin-left: 6%;
    display: flex;
    flex-direction: column;
  }

  h5 {
    color: #ff3e00;
    margin-top: 0;
    margin-bottom: 5px;
    text-align: center;
  }

  .buttons {
    /*background-color: #73b9e8;*/
    width: 100px;
    margin-left: auto;
  }

  input {
    width: 80%;
  }

  .peopleColumn {
    width: 100%;
    height: 65%;
    display: flex;
    flex-direction: column;
  }

  .buttonsBox {
    height: 20px;
  }

  .scrollable {
    flex: 1 1 auto;
    margin: 0 0 0.5em 0;
    overflow-y: auto;
  }

  .scrollable::-webkit-scrollbar-track {
    background: transparent;
  }

  .scrollable::-webkit-scrollbar {
    width: 2px;
    background-color: #eee;
  }

  .scrollable::-webkit-scrollbar-thumb {
    background-color: rgb(168, 168, 168);
  }

  .manBox {
    height: 64px;
    display: flex;
  }

  .manBox:hover {
    background-color: whitesmoke;
  }

  .manBox:active {
    background-color: rgb(238, 238, 238);
  }

  .manBox img {
    height: 60px;
    width: 60px;
    border-radius: 60px;
    margin-top: auto;
    margin-bottom: auto;
  }

  .manBox * {
    margin-left: 10px;
  }

</style>