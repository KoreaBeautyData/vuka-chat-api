<script>
    import { link, push } from 'svelte-spa-router'
    import fastapi from "../src/lib/api"
    import { page } from "../src/lib/store"


    let fine_tune_list = []
    let fine_tune_count = 0;
    let page_length = 7;
    $: total_page = Math.ceil(fine_tune_count/page_length)

    let filename = '';

    function get_fine_tune_list(_page) {
        let params = {
            page: _page,
            page_length: page_length,
        }
        fastapi('get', '/api/fine-tune', params, (json) => {
            fine_tune_list = json.result_data.fine_tune_list
            $page = _page
            fine_tune_count = json.result_data.fine_tune_count
            page_length = json.result_data.page_length
        })
    }

    $: get_fine_tune_list($page);


    function post_faq_csv(event) {
        event.preventDefault()

        let url = "/api/faq/csv"
        let params = {
            filename: filename,
        }

        fastapi('post', url, params, (json) => {
                filename = json.filename
                push("/tuning")
            }
        )
    }

    function post_fine_tune_convert(event) {
        event.preventDefault()

        let url = "/api/fine-tune/convert"
        let params = {
            filename: f_name,
        }

        fastapi('post', url, params, (json) => {
                f_name = json.filename
                push("/tuning")
            }
        )
    }
</script>


<form class="d-flex float-right m-3" role="search" style="width: 30%;">
    <input type="text" class="form-control" bind:value="{filename}">
    <button class="btn btn-outline-secondary ml-2" type="submit" on:click={post_faq_csv} style="width: 50%;">CSV 업로드</button>
</form>

<table class="table table-hover mt-3">
  <thead>
    <tr class="text-center">
      <th scope="col">No</th>
      <th scope="col">id</th>
      <th scope="col">model</th>
      <th scope="col">status</th>
      <th scope="col">fine_tuned_model</th>
      <th scope="col">file</th>
    </tr>
  </thead>
  <tbody>
    {#each fine_tune_list as fine_tune}
    <tr>
      <th scope="row">{fine_tune.id}</th>
      <td><a use:link href="/tuning/{fine_tune.id}">{fine_tune.ft_id}</a></td>
      <td>{fine_tune.model}</td>
      <td>{fine_tune.status}</td>
      <td>{fine_tune.fine_tuned_model}</td>
      <td><a use:link href="/tuning/{fine_tune.id}">{fine_tune.filename}</a></td>
    </tr>
    {/each}
  </tbody>
</table>

<!-- 페이징처리 시작 -->
<ul class="pagination justify-content-center">
    <!-- 이전페이지 -->
    <li class="page-item {$page <= 1 && 'disabled'}">
        <button class="page-link" on:click="{() => get_fine_tune_list($page-1)}">이전</button>
    </li>

    <!-- 페이지번호 -->
    {#each Array(total_page) as _, loop_page}
    {#if loop_page >= $page-5 && loop_page <= $page+5}
    <li class="page-item {loop_page+1 === $page && 'active'}">
        <button on:click="{() => get_fine_tune_list(loop_page+1)}" class="page-link">{loop_page+1}</button>
    </li>
    {/if}
    {/each}

    <!-- 다음페이지 -->
    <li class="page-item {$page > total_page-1 && 'disabled'}">
        <button class="page-link" on:click="{() => get_fine_tune_list($page+1)}">다음</button>
    </li>
</ul>
<!-- 페이징처리 끝 -->