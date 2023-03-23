<script>
    import fastapi from "../src/lib/api"
    import { Jumper } from 'svelte-loading-spinners';

    let result = '';
    let question = '';
    let answer = '';

    function post_chat(event) {
        event.preventDefault()
        let url = "/api/chat/db"
        let params = {
            question: question,
        }
        fastapi('post', url, params,
            (json) => {
                result = json
            }
        )
    }
</script>


<div class="card mb-3" style="height: 50%;">
    {#await answer}
    <p>loading</p>
    {:then answer}
  <div class="card-body">
    <p class="card-text">{result.question}</p>
    <p class="card-text">{result.answer}</p>
  </div>
  {/await}


  <div class="row g-3" style="margin:0 auto;width:100%">
      <div class="col-10">
        <input class="form-control" type="search" placeholder="무엇이든 물어보세요!" bind:value="{question}">
      </div>
      <div class="col">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit" style="margin:10px;" on:click={post_chat}>Send</button>
      </div>
  </div>
</div>