<script>
    import { querystring } from 'svelte-spa-router'
    import fastapi from "../src/lib/api"

    let question = '';
    let answer = '';

    function get_chat() {
        let params = {
            question: question
        }
        fastapi('get', '/api/chat', params, (json) => {
            answer = json
        })
    }
    get_chat();

</script>

<div class="card mb-3" style="height: 50%;">
  <div class="card-body">
    <p class="card-text">{answer}</p>
  </div>

  <form class="form-inline my-2 my-lg-0">
    <input class="form-control mr-sm-2" type="search" placeholder="무엇이든 물어보세요!" bind:value="{question}">
    <button class="btn btn-outline-success my-2 my-sm-0" type="submit" style="margin:10px;" on:click={() => get_chat()}>Send</button>
  </form>
</div>