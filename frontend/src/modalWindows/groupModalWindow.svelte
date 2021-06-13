<script>
  import {groupWindowState} from '../storage.js';
  import {fetches} from "../api";

  let errorMessage = "";
  let groupName = "";
  let stateWindow = true;
  let peoplemass = fetches.get('/users/all'); //TODO
  let newPeopleMass = [];
  $: if ($peoplemass instanceof Promise) $peoplemass.then(v => {$peoplemass = v; newPeopleMass = $peoplemass;})

  function closeWindow() {
    groupWindowState.decrement();
  }

  function nextStep() {
    if (groupName === "") {
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
      <button on:click={closeWindow} class="cancel-button">
        <img src="cancel.svg" class="cancel-icon" alt="cancel-icon" />
      </button>
      <h3>Название группы</h3>
      <input bind:value={groupName}>
      {#if errorMessage !== ""}
        <h5>{errorMessage}</h5>
      {/if}
      <div class="buttons">
        <button on:click={nextStep} class="main-button">Далее</button>
      </div>
    </div>
  {:else}
    <div class="mainBoxSecond">
      <button on:click={closeWindow} class="cancel-button">
        <img src="cancel.svg" class="cancel-icon" alt="cancel-icon" />
      </button>
      <h3>Добавить участников</h3>
      <input on:input={searchContact} placeholder="Поиск">
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
        <button on:click={createFunc} class="main-button">Создать</button>
        <button on:click={prevStep} class="second-button">Отмена</button>
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
    background-color: #343F48;
    border-radius: 8px;
    width: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .mainBoxSecond {
    background-color: whitesmoke;
    width: 300px;
    height: 450px;
    background-color: #343F48;
    /*margin-top: 20%;
    margin-left: calc(50% - 150px);*/
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  h5 {
    color: #E84E58;
    margin-top: 0;
    margin-bottom: 5px;
    text-align: center;
  }

  .main-button {
    background: #07E897;
    color: #343F48;
    font-weight: 500;
    border-radius: 24px;
    padding-left: 12px;
    padding-right: 12px;
    padding-top: 4px;
    padding-bottom: 4px;
    border: none;
    outline: none;
    margin-top: 15px;
    margin-bottom: 15px;
  }

  .second-button {
    border: 1px solid #07E897;
    color: #fff;
    background-color: transparent;
    padding-left: 12px;
    padding-right: 12px;
    padding-top: 4px;
    padding-bottom: 4px;
    outline: none;
    border-radius: 24px;
  }

  input {
    width: 80%;
    background-color: #1B1B1B;
    color: rgba(255, 255, 255, 0.6);
    border-radius: 10px;
    outline: none;
    border: none;
  }

  .peopleColumn {
    width: 100%;
    height: 65%;
    display: flex;
    flex-direction: column;
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
    width: 3px;
    background-color: #1B1B1B;
  }

  .scrollable::-webkit-scrollbar-thumb {
    background-color: var(--darkgreen);
  }

  .manBox {
    height: 64px;
    display: flex;
  }

  .manBox:hover {
    background-color: var(--darkgreen);
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

  .cancel-button {
    display: flex;
    align-items: center;
    justify-content: center;
    align-self: flex-end;
    width: auto;
    margin-right: 10px;
    margin-top: 10px;
    height: 16px;
    padding: 0;
    border: none;
    outline: none;
    background-color: transparent;
}

</style>