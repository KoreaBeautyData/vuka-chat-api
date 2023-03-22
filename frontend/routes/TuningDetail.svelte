<script>
    import fastapi from "../src/lib/api"
    import { push } from 'svelte-spa-router'

    export let params = {}
    let fine_tune_id = params.fine_tune_id
    let fine_tune = {};

    let filename = '';

    function get_fine_tune_detail() {
        fastapi("get", "/api/fine-tune/" + fine_tune_id, {}, (json) => {
            fine_tune = json.result_data.fine_tune
            filename = json.result_data.fine_tune.filename
        })
    }
    get_fine_tune_detail()

    function post_fine_tune_convert(event) {
        event.preventDefault()

        let url = "/api/fine-tune/convert"
        let params = {
            filename: filename,
        }

        fastapi('post', url, params, (json) => {
                push("/tuning/"+fine_tune_id)
            }
        )
    }

    function post_fine_tuning(event) {
        event.preventDefault()

        let url = "/api/fine-tune/tuning"
        let params = {
            filename: filename,
        }

        fastapi('post', url, params, (json) => {
                push("/tuning/"+fine_tune_id)
            }
        )
    }
</script>

<table class="table table-hover mt-3 text-center">
  <thead>
    <tr>
      <th scope="col">No</th>
      <th scope="col">id</th>
      <th scope="col">model</th>
      <th scope="col">status</th>
      <th scope="col">fine_tuned_model</th>
      <th scope="col" colspan="2">file</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">{fine_tune.id}</th>
      <td>{fine_tune.ft_id}</td>
      <td>{fine_tune.model}</td>
      <td>{fine_tune.status}</td>
      <td>{fine_tune.fine_tuned_model}</td>
      <td>
        <form method="post">
          <input type="text" class="form-control" bind:value="{fine_tune.filename}">
        </form>
      </td>
      <td>
        <button class="btn btn-outline-info mr-5" on:click="{post_fine_tune_convert}">변환</button>
        <button class="btn btn-outline-success" on:click="{post_fine_tuning}">튜닝</button>
      </td>
    </tr>
  </tbody>
</table>
