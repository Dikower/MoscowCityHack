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

<div class="WindowBox">

    <div class="mainBoxSecond">
      <h3>Contacts</h3>
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
        <button>Add contact</button>
        <button on:click={createFunc}>close</button>
      </div>
    </div>
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

  .mainBoxSecond {
    background-color: whitesmoke;
    width: 300px;
    height: 450px;
    /*margin-top: 20%;*/
    /*margin-left: calc(50% - 150px);*/
    margin-top: 4%;
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

  .deleteButton{
    background-color: #ff3e00;
    width: 15px;
    height: 15px;
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