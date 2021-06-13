<script>
  import {beforeUpdate, afterUpdate} from 'svelte';

  let comments = [
    {author: 'user', text: "Привет", like: false},
    {author: 'recipient', text: "Привет", like: false},
    {author: 'user', text: "Как дела?", like: false},
    {author: 'recipient', text: "Пока не родила!", like: false},
    {author: 'user', text: "Привет", like: false},
    {author: 'recipient', text: "Привет", like: false},
    {author: 'user', text: "Как дела?", like: false},
    {author: 'recipient', text: "Пока не родила!", like: false},
    {author: 'user', text: "Привет", like: false},
    {author: 'recipient', text: "Привет", like: false},
    {author: 'user', text: "Как дела?", like: false},
    {author: 'recipient', text: "Пока не родила!", like: false},
    {author: 'user', text: "Привет", like: false},
    {author: 'recipient', text: "Привет", like: false},
    {author: 'user', text: "Как дела?", like: false},
    {author: 'recipient', text: "Пока не родила!", like: false}
  ];

  export let recipientName = "Имя";
  export let recipientImg = "";
  let userImg = "http://sun9-57.userapi.com/s/v1/ig2/05fFA-EaTmuVYZZr-ffFFe5rerv4-qNX7amMwstHpboPHm3HPWwQruNwP0MkyJNgU3rJxAr-npGMvnFfx0sqK4ng.jpg?size=400x0&quality=96&crop=0,152,960,994&ava=1"
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



  function handleClick(number) {
    console.log(number);
    let m = comments;
    m[number].like = !m[number].like;
    comments = m;
  }

</script>


<div class="chat">
  <div class="header">
    <h2>{recipientName}</h2>
    <div>
      <img src={recipientImg} class="recImg">
      <img src={userImg} class="userImg">
    </div>
  </div>
  <div class="scrollable" bind:this={div}>
    {#each comments as comment, number}
      <div on:dblclick={() => handleClick(number)}>
        <article class={comment.author}>
          <span>{comment.text}</span>
        </article>
        {#if (comment.like)&&(comment.author)==="user"}
          <img src="heart.svg" class="userLikeImg">
        {:else if (comment.like)&&(comment.author)==="recipient"}
          <img src="heart.svg" class="recipientLikeImg">
        {/if}
      </div>

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
    height: 40px;
    display: flex;
    flex-direction: row;
    padding: 10px;
    justify-content: space-between;
    align-items: center;
  }

  .header img {
    height: 40px;
    width: 40px;
    border-radius: 60px;
    margin-top: auto;
    margin-bottom: auto;
  }

  .recImg{
    z-index: 100;
    border: #999999 solid 2px;
  }

  .userImg{
    margin-left: -20px;
    border: #12BBA6 solid 2px;
    z-index: 200;
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
    height: 24px;
    width: 24px;
  }

  .message-icon {
    width: 16px;
    height: 18px;
  }

  .audio-icon {
    height: 24px;
    width: 24px;
  }

  .photo-icon {
    width: 24px;
    height: 24px;
  }

  .user {
    text-align: right;
    margin-bottom: -25px;
    margin-top: 35px;
  }
  .userLikeImg{
    margin-left: calc(100% - 30px);
    margin-bottom: -20px;
    height: 20px;
    width: 20px;
  }
  span {
    padding: 0.5em 1em;
    display: inline-block;
  }
  .recipient{
    margin-bottom: -25px;
    margin-top: 35px;
  }
  .recipientLikeImg{
    margin-left: 10px;
    margin-bottom: -20px;
    height: 20px;
    width: 20px;
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

  .sendPhoto:hover {
    background-color: #375EC9;
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
    background: var(--darkgreenwithopacity);
    color: #fff;
    border-radius: 1em 1em 0 1em;
    word-break: break-all;
  }

</style>