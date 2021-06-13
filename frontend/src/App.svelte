<script>
  import Chat from "./chatField.svelte";
  import Settings from "./modalWindows/settingsModalWindow.svelte";
  import Channel from "./modalWindows/channelModalWindow.svelte";
  import Contacts from "./modalWindows/contactsModalWindow.svelte";
  import Group from "./modalWindows/groupModalWindow.svelte";
  import Auth from './authWindow.svelte';
  import Moveable from "svelte-moveable";
  import {fetches} from "./api";
  import {onMount} from 'svelte';
  import {channelWindowState, contactsWindowState, groupWindowState, settingWindowState, ID} from './storage.js';

  const frame = {
    translate: [0, 0],
  };
  let target;

  let recipientName = "";
  let recipientImg = "";
  let settingState = 0;
  onMount(async () =>{
    ID.set(localStorage.getItem("ID"));
  });
  // let userID = "тут мог быть ваш уникальный ID";

  let peoplemass = fetches.get('/users/all');
  let newPeopleMass = [];
  $: if ($peoplemass instanceof Promise) $peoplemass.then(v => {$peoplemass = v; newPeopleMass = $peoplemass;})
  $: console.log('update', $peoplemass)

  function funcChoiceChat(name, img) {
    if(h>w){
      stateDopTap = !stateDopTap;
    }
    recipientName = name;
    recipientImg = img;
  }

  function openSettings() {
    settingState = !settingState;
  }

  function openSettingsWindow() {
    settingWindowState.increment();
  }

  function openGroupWindow() {
    groupWindowState.increment();
  }

  function openChannelWindow() {
    channelWindowState.increment();
  }

  function openContactsWindow() {
    contactsWindowState.increment();
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
      })
    }
  }
  let stateDopTap = false;
  function openDopTap(){
    stateDopTap = !stateDopTap;
  }
  let w;
  let h;
</script>

<svelte:window bind:innerHeight={h} bind:innerWidth={w}/>
<div class="mainBox" bind:this={target}>
  {#if ($ID === "")||($ID === null)}
    <Auth/>
  {:else}
    <div class="boxForModalWindow">
      {#if $settingWindowState === 1}
        <Settings/>
      {/if}
      {#if $channelWindowState === 1}
        <Channel/>
      {/if}
      {#if $contactsWindowState === 1}
        <Contacts/>
      {/if}
      {#if $groupWindowState === 1}
        <Group/>
      {/if}
    </div>

    <div class="controlPanel">

      {#if h<w}
        <img src="settings.svg" alt="settings" class="settingIcon" on:click={openSettings}>
        <input on:input={searchContact} class="settingInput" placeholder="Search">
      {:else}
        {#if !stateDopTap}
          <img src="arrow.svg" alt="settings" class="settingIcon" on:click={openDopTap}>
        {:else}
          <img src="settings.svg" alt="settings" class="settingIcon" on:click={openSettings}>
          <input on:input={searchContact} class="settingInput" placeholder="Search">

        {/if}
      {/if}
      <img src="logo.svg" class="logo" alt="logo" />

    </div>
    <div class="infoBox">
      {#if h<w}
        {#if (!settingState)}
          <div class="peopleColumn">
            <div class="scrollable">
              {#await $peoplemass}
              {:then data}
                {#each newPeopleMass as man}
                  <div class="manBox" on:click={() => funcChoiceChat(man.fio, man.avatar)}>
                    <img src={man.avatar} alt="Avatar" class="man-img-online">
                    <div class="person-info">
                      <h3>{man.fio}</h3>
                      <p>Online</p>
                    </div>
                  </div>
                  <hr>
                {/each}
              {/await}
            </div>
          </div>
        {:else }
          <div class="settingsColumn">
            <div class="SettingsTab" on:click={openGroupWindow}>
              <h3>Создать группу</h3>
            </div>
            <div class="SettingsTab" on:click={openChannelWindow}>
              <h3>Создать канал</h3>
            </div>
            <div class="SettingsTab" on:click={openContactsWindow}>
              <h3>Контакты</h3>
            </div>
            <div class="SettingsTab" on:click={openSettingsWindow}>
              <h3>Настройки</h3>
            </div>
          </div>
        {/if}

        {#if recipientName === ""}
          <h4 class="message">Please select a chat to start messaging</h4>
        {:else}
          <Chat {recipientName} {recipientImg}/>
        {/if}
      {:else}
        {#if !stateDopTap}
          {#if recipientName === ""}
            <h4 class="message">Please select a chat to start messaging</h4>
          {:else}
            <Chat {recipientName} {recipientImg}/>
          {/if}
        {:else}
          {#if !settingState}
            <div class="peopleColumn" style="width: 100%">
              <div class="scrollable">
                {#await $peoplemass}
                {:then data}
                  {#each newPeopleMass as man}
                    <div class="manBox" on:click={() => funcChoiceChat(man.name, man.img)}>
                      <img src={man.img} alt="Avatar">
                      <div class="person-info">
                        <h4>{man.name}</h4>
                        <p>Online</p>
                      </div>
                    </div>
                    <hr>
                  {/each}
                {/await}
              </div>
            </div>
          {:else}
            <div class="settingsColumn" style="width: 100%">
              <div class="SettingsTab" on:click={openGroupWindow}>
                <h3>Создать группу</h3>
              </div>
              <div class="SettingsTab" on:click={openChannelWindow}>
                <h3>Создать канал</h3>
              </div>
              <div class="SettingsTab" on:click={openContactsWindow}>
                <h3>Контакты</h3>
              </div>
              <div class="SettingsTab" on:click={openSettingsWindow}>
                <h1>Настройки</h1>
              </div>
            </div>
          {/if}
        {/if}
      {/if}
    </div>
  {/if}

</div>

<!--<Moveable-->
<!--    target={target}-->
<!--    resizable={true}-->
<!--    throttleResize={10}-->
<!--    on:resizeStart={({ detail: {target, set, setOrigin, dragStart }}) => {-->
<!--        // Set origin if transform-origin use %.-->
<!--		setOrigin(["%", "%"]);-->
<!--        // If cssSize and offsetSize are different, set cssSize. (no box-sizing)-->
<!--        const style = window.getComputedStyle(target);-->
<!--        const cssWidth = parseFloat(style.width);-->
<!--        const cssHeight = parseFloat(style.height);-->
<!--        set([cssWidth, cssHeight]);-->

<!--        // If a drag event has already occurred, there is no dragStart.-->
<!--        dragStart && dragStart.set(frame.translate);-->
<!--    }}-->
<!--    on:resize={({ detail: { target, width, height, drag }}) => {-->
<!--        target.style.width = `${width}px`;-->
<!--        target.style.height = `${height}px`;-->

<!--        // get drag event-->
<!--        frame.translate = drag.beforeTranslate;-->
<!--        target.style.transform-->
<!--            = `translate(${drag.beforeTranslate[0]}px, ${drag.beforeTranslate[1]}px)`;-->
<!--    }}-->
<!--    on:resizeEnd={({ detail: { target, isDrag, clientX, clientY }}) => {-->
<!--        console.log("onResizeEnd", target, isDrag);-->
<!--    }}-->
<!--/>-->

<style >
  .mainBox {
    width: 520px;
    height: 600px;
    border: #343F48 solid 0.5px;
    margin: auto;
  }

  .logo {
    height: 40px;
    width: 40px;
    margin-left: auto;
    margin-right: 10px;
  }

  /*.boxForModalWindow{*/
  /*  !*background-color: red;*!*/
  /*  position: absolute;*/
  /*  width: 100%;*/
  /*  height: 100%;*/
  /*}*/

  hr {
    border: 0.05px solid rgba(60, 60, 67, 0.29);
  }

  .controlPanel {
    height: 60px;
    width: 100%;
    min-width: 400px;
    background: var(--darkgreen);
    display: flex;
    align-items: center;
  }

  .settingIcon {
    height: 30px;
    width: 30px;
    float: right;
    margin-left: 10px;
  }

  .person-info {
    align-items: left;
    text-align: left;
    line-height: 0;
  }

  .person-info p {
    color: var(--darkgreen);
  }

  .man-img-online {
    border: 2px solid var(--darkgreen);
  }

  .scrollable p {
    font-size: calc(8px + (10 - 8) * ((100vw - 300px) / (1440 - 300)));
  }

  .settingInput {
    margin-left: 10px;
    width: calc(40% - 60px);
    background-color: #343F48;
    outline: none;
    border: none;
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.6);
  }

  .infoBox {
    display: flex;
    width: 100%;
    height: calc(100% - 60px);
    flex-direction: row;
  }

  .peopleColumn {
    width: 40%;
    /*max-width: 300px;*/
    min-width: 200px;
    height: 100%;
    display: flex;
    flex-direction: column;
    background-color: #343F48;
  }

  .settingsColumn {
    width: 40%;
    background-color: #343F48;
    /*max-width: 300px;*/
    min-width: 200px;
    height: 100%;
    border-right-color: #343F48;
    border-right-style: solid; /* Стиль линии */
    border-right-width: 1px;
    display: flex;
    flex-direction: column;
  }

  .SettingsTab {
    display: flex;
    height: 50px;
    margin-top: 10px;
    align-items: center;
    text-align: center;
    /*background-color: #666666;*/
  }

  .SettingsTab:hover {
    background-color: var(--darkgreenwithopacity);
  }

  .SettingsTab:active {
    background-color: rgba(245, 245, 245, 0.3);
  }

  .settingsIcon {
    height: 45px;
    width: 45px;
    margin-top: auto;
    margin-bottom: auto;
    margin-left: 10px;
  }

  .SettingsTab h3 {
    color: #f5f5f5;
    margin-left: 15px;
    margin-top: 12px;
    font-weight: 500;
    text-align: center;
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
    background-color: #A0A0A0;
  }

  .scrollable::-webkit-scrollbar-thumb {
    background-color: var(--darkgreen);
  }

  .manBox {
    height: 64px;
    display: flex;
    text-align: center;
    padding: 2px;
    align-items: center;
    margin-top: -6px;
  }

  .manBox:hover {
    background-color: var(--darkgreenwithopacity);
    color: #fff;
  }

  .manBox:active {
    background-color: #343F48;
  }

  .manBox img {
    height: 50px;
    width: 50px;
    border-radius: 60px;
    margin-top: auto;
    margin-bottom: auto;
  }

  .manBox * {
    margin-left: 5px;
  }

  .message {
    margin: auto;
    color: grey;
  }
</style>