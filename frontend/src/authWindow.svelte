<script>
  import {ID} from "./storage";
  function up(){
    localStorage.setItem("ID", "2e23:de42:de52:aw41");
    ID.set("2e23:de42:de52:aw41");
  }
</script>


<h1>Auth</h1>
<button on:click={up}></button>