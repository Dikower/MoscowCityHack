<script>
  import {beforeUpdate, afterUpdate} from 'svelte';

  let comments = [
    {author: 'user', text: "Привет"},
    {author: 'recipient', text: "Привет"},
    {author: 'user', text: "Как дела?"},
    {author: 'recipient', text: "Пока не родила!"},
    {author: 'user', text: "Привет"},
    {author: 'recipient', text: "Привет"},
    {author: 'user', text: "Как дела?"},
    {author: 'recipient', text: "Пока не родила!"},
    {author: 'user', text: "Привет"},
    {author: 'recipient', text: "Привет"},
    {author: 'user', text: "Как дела?"},
    {author: 'recipient', text: "Пока не родила!"},
    {author: 'user', text: "Привет"},
    {author: 'recipient', text: "Привет"},
    {author: 'user', text: "Как дела?"},
    {author: 'recipient', text: "Пока не родила!"}
  ];

  export let recipientName = "Имя";
  export let recipientImg = "";
  let div;
  let autoscroll;
  let messageField;

  beforeUpdate(() => {
    autoscroll = div && (div.offsetHeight + div.scrollTop) > (div.scrollHeight - 20);
  });

  afterUpdate(() => {
    if (autoscroll) div.scrollTo(0, div.scrollHeight);
  });

  function handleKeydown(event) {
    if (event.key === 'Enter') {
      const text = event.target.value;
      if (!text) return;

      comments = comments.concat({
        author: 'user',
        text
      });

      event.target.value = '';
    }
  }
  function send(){
    const text = messageField;
    if (!text) return;

    comments = comments.concat({
      author: 'user',
      text
    });

    messageField = '';
  }
</script>


<div class="chat">
  <div class="header">
    <h1>{recipientName}</h1>
    <img
        src={recipientImg}
        alt="">
  </div>
  <div class="scrollable" bind:this={div}>
    {#each comments as comment}
      <article class={comment.author}>
        <span>{comment.text}</span>
      </article>
    {/each}
  </div>
  <div class="senderPanel">
    <button class="sendEmoji">
      <img src="Emoji.svg" class="emoji-icon" alt="emoji-icon" />
    </button>
    <button class="sendEmoji">
      <img src="Audio.svg" class="audio-icon" alt="audio-icon" />
    </button>
    <textarea on:keydown={handleKeydown} placeholder="Write a message..." bind:value={messageField}></textarea>
    <button class="sendMessage" on:click={send}>
      <img src="message.svg" class="message-icon" alt="message-icon" />
    </button>
    <button class="sendPhoto" on:click={send}>
      <img src="photo.svg" class="photo-icon" alt="photo-icon" />
    </button>
  </div>
</div>


<style>

  .chat {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    /* border: black solid 1px; */
  }

  .header {
    height: 80px;
    display: flex;
    flex-direction: row;
    padding: 10px;
    justify-content: space-around;
    align-items: center;
  }

  img {
    height: 50px;
    width: 50px;
    border-radius: 60px;
    margin-top: auto;
    margin-bottom: auto;
  }

  .scrollable {
    flex: 1 1 auto;
    border-top: 1px solid #343F48;
    margin: 0 0 0.5em 0;
    overflow-y: auto;
    padding: 10px;
    /* scrollbar-width: auto; "auto" or "thin"  */
  }

  .scrollable::-webkit-scrollbar-track {
    background: transparent;
  }

  .scrollable::-webkit-scrollbar {
    width: 5px;
    background-color: #343F48;
  }

  .scrollable::-webkit-scrollbar-thumb {
    border-radius: 20px;
    background-color: var(--darkgreen);
  }

  article {
    margin: 0.5em 0;
  }
  
  .emoji-icon {
    height: 27px;
    width: 27px;
  }

  .message-icon {
    width: 16px;
    height: 18px;
  }

  .audio-icon {
    height: 24px;
    width: 40px;
  }

  .photo-icon {
    width: 18px;
    height: 16px;
  }

  .user {
    text-align: right;
  }

  span {
    padding: 0.5em 1em;
    display: inline-block;
  }

  .recipient span {
    background-color: #343F48;
    border-radius: 1em 1em 1em 0;
  }
  .senderPanel{
    /*background-color: #73b9e8;*/
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 10px;
  }
  .senderPanel textarea{
    height: 40px;
    width: calc(80% - 40px);
    background-color: #343F48;
    color: rgba(255, 255, 255, 0.6);
    border: none;
    outline:none;
    border-radius: 10px;
    overflow: hidden;
    resize:none;
    padding-right: 40px;
    padding-left: 10px;
    font-size: calc(10px + (12 - 10) * ((100vw - 300px) / (1440 - 300)));
  }

  .sendPhoto {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    vertical-align: middle;
    height: 40px;
    width: 40px;
    border-radius: 10px;
    outline: none;
    border: none;
    background-color: var(--darkgreen);
    margin-left: 10px;
  }

  .sendEmoji {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    vertical-align: middle;
    height: 40px;
    width: 30px;
    margin-right: 5px;
    background-color: transparent;
    border: none;
    outline: none;
  }

  .sendMessage{
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1px;
    margin-left: -37px;
    height: 40px;
    width: 40px;
    border-radius: 10px;
    outline: none;
    border: none;
    background: rgba(160, 160, 160, 0.3);
  }

  .sendMessage:hover {
    background-color: #375EC9;
  }

  .user span {
    background: var(--darkgreen);
    color: #fff;
    border-radius: 1em 1em 0 1em;
    word-break: break-all;
  }

</style>