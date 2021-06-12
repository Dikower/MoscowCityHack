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
        src="http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
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
    <input on:keydown={handleKeydown} placeholder="Write a message..." bind:value={messageField}>
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
    justify-content: space-around;
  }

  img {
    height: 60px;
    width: 60px;
    border-radius: 60px;
    margin-top: auto;
    margin-bottom: auto;
  }

  .scrollable {
    flex: 1 1 auto;
    border-top: 1px solid #eee;
    margin: 0 0 0.5em 0;
    overflow-y: auto;
    /* scrollbar-width: auto; "auto" or "thin"  */
  }

  .scrollable::-webkit-scrollbar-track {
    background: transparent;
  }

  .scrollable::-webkit-scrollbar {
    width: 7px;
    background-color: #eee;
  }

  .scrollable::-webkit-scrollbar-thumb {
    border-radius: 20px;
  }

  article {
    margin: 0.5em 0;
  }

  .message-icon {
    width: 16px;
    height: 18px;
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
  }
  .senderPanel input{
    height: 40px;
    width: calc(100% - 40px);
    background-color: #343F48;
    color: rgba(255, 255, 255, 0.6);
    border: none;
    outline:none;
    border-radius: 10px;
    padding: 20px;
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
    background-color: #07CC85;
  }

  .sendMessage{
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    vertical-align: middle;
    margin-left: -40px;
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
    background: #07CC85;
    color: #fff;
    border-radius: 1em 1em 0 1em;
    word-break: break-all;
  }

</style>