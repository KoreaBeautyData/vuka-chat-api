<script>
    import fastapi from "../src/lib/api"

    let fine_tuned_model = ''

    let result = '';
    let question = '';
    let answer = '';

    function post_chat(event) {
        event.preventDefault()
        let url = "/api/chat"
        let params = {
            question: question,
            fine_tuned_model: fine_tuned_model,
        }
        fastapi('post', url, params,
            (json) => {
                result = json
            }
        )
    }

    let fine_tune_model_list = '';

    function get_fine_tune_model_list() {
        fastapi('get', '/api/fine-tune/model', {}, (json) => {
            fine_tune_model_list = json.result_data.fine_tune_model_list
        })
    }
    console.log(fine_tune_model_list);
    get_fine_tune_model_list();
</script>


<div class="card mb-3" style="height: 50%;">
  <div class="card-body">
    <p class="card-text">Q: {result.question}</p>
    <p class="card-text">A: {result.answer}</p>
  </div>

  <div class="row g-3" style="margin:0 auto;width:100%">
      <div class="col-3">
        <input class="form-control" type="search" placeholder="fine_tuned_model" bind:value="{fine_tuned_model}">
      </div>
      <div class="col-7">
        <input class="form-control" type="search" placeholder="무엇이든 물어보세요!" bind:value="{question}">
      </div>
      <div class="col">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit" style="margin:10px;" on:click={post_chat}>Send</button>
      </div>
  </div>
</div>