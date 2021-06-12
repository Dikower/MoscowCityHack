<script>
  import Chat from "./chatField.svelte";
  import Settings from "./modalWindows/settingsModalWindow.svelte";
  import Channel from "./modalWindows/channelModalWindow.svelte";
  import Contacts from "./modalWindows/contactsModalWindow.svelte";
  import Group from "./modalWindows/groupModalWindow.svelte";

  import Moveable from "svelte-moveable";
  import {channelWindowState, contactsWindowState, groupWindowState, settingWindowState} from './storage.js';

  const frame = {
    translate: [0, 0],
  };
  let target;

  let recipientName = "";
  let settingState = 0;
  let peoplemass = [{
    name: "Фёдор",
    img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
  },
    {
      name: "Диана",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Света",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Иван",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Мистер Х",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Федор",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Диана",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },

    {
      name: "Иван",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Мистер Х",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Федор",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Диана",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Света",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Иван",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Света",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Иван",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    },
    {
      name: "Мистер Х",
      img: "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
    }];
  let newPeopleMass = peoplemass;

  function funcChoiceChat(name) {
    recipientName = name;
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
      newPeopleMass = peoplemass;
    } else {
      newPeopleMass = [];
      peoplemass.forEach(element => {
        let elName = element.name.toLowerCase();
        if (elName.indexOf(reqName.toLowerCase()) !== -1) {
          newPeopleMass = newPeopleMass.concat(element);
        }
      })
    }
  }
</script>


<div class="mainBox" bind:this={target}>
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
    <img src="setting-lines.svg" class="settingIcon" on:click={openSettings}>
    {#if !settingState}
      <input on:input={searchContact} class="settingInput" placeholder="Search">
    {/if}
  </div>
  <div class="infoBox">
    {#if (!settingState)}
      <div class="peopleColumn">
        <div class="scrollable">
          {#each newPeopleMass as man}
            <div class="manBox" on:click={() => funcChoiceChat(man.name)}>
              <img src={man.img} alt="">
              <h4>{man.name}</h4>
            </div>
          {/each}
        </div>
      </div>
    {:else }
      <div class="settingsColumn">
        <div class="SettingsTab" on:click={openGroupWindow}>
          <img src="settings.svg" class="settingsIcon">
          <h3>New Group</h3>
        </div>
        <div class="SettingsTab" on:click={openChannelWindow}>
          <img src="settings.svg" class="settingsIcon">
          <h3>New Channel</h3>
        </div>
        <div class="SettingsTab" on:click={openContactsWindow}>
          <img src="settings.svg" class="settingsIcon">
          <h3>Contacts</h3>
        </div>
        <div class="SettingsTab" on:click={openSettingsWindow}>
          <img src="settings.svg" class="settingsIcon">
          <h3>Settings</h3>
        </div>
      </div>
    {/if}

    {#if recipientName === ""}
      <h4 class="message">Please select a chat to start messaging</h4>
    {:else}
      <Chat {recipientName}/>
    {/if}
  </div>
</div>

<Moveable
    target={target}
    resizable={true}
    throttleResize={10}
    on:resizeStart={({ detail: {target, set, setOrigin, dragStart }}) => {
        // Set origin if transform-origin use %.
		setOrigin(["%", "%"]);
        // If cssSize and offsetSize are different, set cssSize. (no box-sizing)
        const style = window.getComputedStyle(target);
        const cssWidth = parseFloat(style.width);
        const cssHeight = parseFloat(style.height);
        set([cssWidth, cssHeight]);

        // If a drag event has already occurred, there is no dragStart.
        dragStart && dragStart.set(frame.translate);
    }}
    on:resize={({ detail: { target, width, height, drag }}) => {
        target.style.width = `${width}px`;
        target.style.height = `${height}px`;

        // get drag event
        frame.translate = drag.beforeTranslate;
        target.style.transform
            = `translate(${drag.beforeTranslate[0]}px, ${drag.beforeTranslate[1]}px)`;
    }}
    on:resizeEnd={({ detail: { target, isDrag, clientX, clientY }}) => {
        console.log("onResizeEnd", target, isDrag);
    }}
/>

<style>

  .mainBox {
    width: 520px;
    height: 600px;
    border: black solid 1px;
    margin: auto;
  }

  /*.boxForModalWindow{*/
  /*  !*background-color: red;*!*/
  /*  position: absolute;*/
  /*  width: 100%;*/
  /*  height: 100%;*/
  /*}*/

  .controlPanel {
    height: 60px;
    width: 100%;
    min-width: 400px;
    background-color: #73b9e8;
  }

  .settingIcon {
    height: 30px;
    width: 30px;
    margin-top: 15px;
    margin-left: 15px;
  }

  .settingInput {
    margin-left: 10px;
    width: calc(40% - 60px);
    height: 30px;
    max-width: 240px;
    min-width: 140px;
  }

  .infoBox {
    display: flex;
    width: 100%;
    height: calc(100% - 60px);
    flex-direction: row;
  }

  .peopleColumn {
    width: 40%;
    max-width: 300px;
    min-width: 200px;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .settingsColumn {
    width: 40%;
    max-width: 300px;
    min-width: 200px;
    height: 100%;
    border-right-color: #eee;
    border-right-style: solid; /* Стиль линии */
    border-right-width: 1px;
    display: flex;
    flex-direction: column;
  }

  .SettingsTab {
    display: flex;
    height: 50px;
    margin-top: 10px;
    /*background-color: #666666;*/
  }

  .SettingsTab:hover {
    background-color: whitesmoke;
  }

  .SettingsTab:active {
    background-color: rgb(238, 238, 238);
  }

  .settingsIcon {
    height: 45px;
    width: 45px;
    margin-top: auto;
    margin-bottom: auto;
    margin-left: 10px;
  }

  .SettingsTab h3 {
    color: #727272;
    margin-left: 15px;
    margin-top: 12px;
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

  .message {
    margin: auto;
    color: grey;
  }
</style>