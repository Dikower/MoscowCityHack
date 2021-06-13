<script>
  import {contactsWindowState} from '../storage.js';
  import {fetches} from "../api";

  let errorMessage = "";
  let channelName = "";
  // let stateWindow = true;
  let peoplemass = fetches.get('/users/all'); //TODO
  let newPeopleMass = [];
  $: if ($peoplemass instanceof Promise) $peoplemass.then(v => {$peoplemass = v; newPeopleMass = $peoplemass;})

  function closeWindow() {
    contactsWindowState.decrement();
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

<div id="TB_overlay"></div>
<div class="WindowBox">

    <div class="mainBoxSecond">
      <button on:click={closeWindow} class="cancel-button">
        <img src="cancel.svg" class="cancel-icon" alt="cancel-icon" />
      </button>
      <h3>Контакты</h3>
      <input on:input={searchContact}>
      <div class="peopleColumn">
        <div class="scrollable">
          {#await $peoplemass}
          {:then data}
            {#each newPeopleMass as man}
              <div class="manBox">
                <img src={man.img} alt="">
                <h4>{man.name}</h4>
                <button class="deleteButton"></button>
              </div>
            {/each}
          {/await}
        </div>
      </div>
      <div class="buttonsBox">
        <button class="main-button">Добавить контакт</button>
      </div>
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

  .WindowBox {
    position: absolute;
    /*background-color: #999999;*/
    /*opacity: 0.7;*/
    z-index: 101;
    /*z-index:3;*/
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

  .mainBoxSecond {
    position: absolute;
    background-color: #343F48;
    width: 300px;
    height: 500px;
    left: 50%;
    display: flex;
    align-items: center;
    flex-direction: column;
    border-radius: 8px;
    padding: 10px;
  }

  h5 {
    color: #ff3e00;
    margin-top: 0;
    margin-bottom: 5px;
    text-align: center;
  }

  .deleteButton{
    background-color: #ff3e00;
    width: 15px;
    height: 15px;
    margin-left: auto;
  }

  input {
    width: 80%;
    background-color: #1B1B1B;
    color: rgba(255, 255, 255, 0.6);
    border-radius: 10px;
    outline: none;
    border: none;
    margin-bottom: 15px;
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
    background-color: var(--darkgreenwithopacity);
  }

  .manBox:active {
    background-color: rgba(245, 245, 245, 0.3);
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