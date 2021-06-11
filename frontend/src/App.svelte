<script>
  let recipientName = "";
  let settingState = 0;
  let peoplemass = [];

  function funcChoiceChat(name) {
    recipientName = name;
  }

  function openSettings() {
    settingState = !settingState;
  }
</script>

<div>
  <div>
    <input class="settingInput" placeholder="Search">
  </div>
  <div>
    {#if (!settingState)}
      <div>
        <div>
          {#each peoplemass as man}
            <div on:click={() => funcChoiceChat(man.name)}>
              <h4>Account name</h4>
            </div>
          {/each}
        </div>
      </div>
    {:else }
      <div>
        <div>
          <h3>Settings</h3>
        </div>
      </div>
    {/if}

    {#if recipientName === ""}
      <h4>Please select a chat to start messaging</h4>
    {:else}
      //тут будет чат
    {/if}
  </div>
</div>