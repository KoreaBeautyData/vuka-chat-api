<script>
    import fastapi from "../src/lib/api"

    let result = '';
    let question = '';
    let answer = '';

    function post_chat(event) {
        event.preventDefault()
        let url = "/api/chat"
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
  <div class="card-body">
    <p class="card-text">Q: {result.question}</p>
    <p class="card-text">A: {result.answer}</p>
  </div>

  <form class="form-inline my-2 my-lg-0" method="post">
    <input class="form-control mr-sm-2" type="search" placeholder="무엇이든 물어보세요!" bind:value="{question}">
    <button class="btn btn-outline-success my-2 my-sm-0" type="submit" style="margin:10px;" on:click={post_chat}>Send</button>
  </form>
</div>