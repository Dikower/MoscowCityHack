<script>
  import {channelWindowState} from '../storage.js';
  import {fetches} from "../api";

  let errorMessage = "";
  let channelName = "";
  let stateWindow = true;
  let peoplemass = fetches.get('/users/all'); //TODO
  let newPeopleMass = [];
  $: if ($peoplemass instanceof Promise) $peoplemass.then(v => {
    $peoplemass = v;
    newPeopleMass = $peoplemass;
  })

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
        let elName = element.fio.toLowerCase();
        if (elName.indexOf(reqName.toLowerCase()) !== -1) {
          newPeopleMass = newPeopleMass.concat(element);
        }
      });
    }
  }
</script>

<div id="TB_overlay">
</div>

<div class="wrapper">
  <div class="WindowBox">
    {#if stateWindow}
      <div class="mainBox">
        <button on:click={closeWindow} class="cancel-button">
          <img src="cancel.svg" class="cancel-icon" alt="cancel-icon"/>
        </button>
        <h3>Название канала</h3>
        <input bind:value={channelName}>
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
          <img src="cancel.svg" class="cancel-icon" alt="cancel-icon" style="margin-top: 40px"/>
        </button>
        <h3>Добавление участников в {channelName}</h3>
        <input on:input={searchContact}>
        <div class="peopleColumn">
          <div class="scrollable">
            {#await $peoplemass}
            {:then data}
              {#each newPeopleMass as man}
                <div class="manBox">
                  <img src={man.avatar} alt="">
                  <h4>{man.fio}</h4>
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
</div>

<style>
  #TB_overlay {
    background-color: #000; /* Чёрный фон */
    height: 100%; /* Высота максимальна */
    left: 0; /* Нулевой отступ слева */
    opacity: 0.50; /* Степень прозрачности */
    position: fixed; /* Фиксированное положение */
    top: 0; /* Нулевой отступ сверху */
    width: 100%; /* Ширина максимальна */
    z-index: 100; /* Заведомо быть НАД другими элементами */
  }

  .wrapper {
    position: relative;
  }

  .WindowBox {
    position: absolute;
    top: 0;
    left: 0;
    height: 500px; /* FIXME подумать, как сделать лучше */
    width: 100%;
    display: grid;
    z-index: 101;
    place-items: center;
  }

  .mainBox {
    background-color: #343F48;
    border-radius: 8px;
    width: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    /*margin-top: 20%;*/
    /*margin-left: calc(50% - 150px);*/
  }

  .mainBoxSecond {
    width: 300px;
    height: 450px;
    background-color: #343F48;
    margin-top: 20%;
    /*margin-left: calc(50% - 150px);*/
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

  .buttonsBox {
    padding-bottom: 20px;
  }
</style>