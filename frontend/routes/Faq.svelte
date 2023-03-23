<script>
    import { link } from 'svelte-spa-router'
    import fastapi from "../src/lib/api"
    import { page } from "../src/lib/store"

    let faq_list = [];
    let faq_count = 0;
    let page_length = 7;
    let kw = ''
    $: total_page = Math.ceil(faq_count/page_length)

    function get_faq_list(_page) {
        let params = {
            page: _page,
            page_length: page_length,
            keyword: kw,
        }
        fastapi('get', '/api/faq', params, (json) => {
            faq_list = json.result_data.faq_list
            $page = _page
            faq_count = json.result_data.faq_count
        })
    }
    $: get_faq_list($page);

    function delete_faq_detail(faq_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {

            let url = "/api/faq/" + faq_id
            let params = {
                faq_id: faq_id
            }
            fastapi('delete', url, params, (json) => {
                    push('/faq')
                }
            )
        }
    }

    function post_faq_csv(event) {
        event.preventDefault()

        fastapi('post', "/api/faq/csv", {}, (json) => {
                push("/faq")
            }
        )
    }
</script>

<nav class="navbar bg-body-tertiary mb-3 mt-3">
  <div class="container-fluid">
    <a use:link href="/faq/create" class="btn btn-outline-info">FAQ 등록</a>
    <form class="d-flex" role="search">
      <input type="text" class="form-control float-right mr-3" bind:value="{kw}" style="width:70%">
      <button class="btn btn-outline-secondary" on:click={() => get_faq_list(1)}>Search</button>
    </form>
  </div>
</nav>

<table class="table table-hover">
  <thead>
    <tr>
      <th scope="col">ID</th>
      <th scope="col">Question</th>
      <th scope="col" colspan="2"></th>
    </tr>
  </thead>
  <tbody>
    {#each faq_list as faq}
    <tr>
      <th scope="row">{faq.id}</th>
      <td><a use:link href="/faq/{faq.id}">{faq.question}</a></td>
      <td><button class="btn btn-outline-danger float-right" on:click={() => delete_faq_detail(faq.id)}>삭제</button></td>
      <td><a use:link href="/faq/modify/{faq.id}" class="btn btn-outline-warning float-right mr-2">수정</a></td>
    </tr>
    {/each}
  </tbody>
</table>

<!-- 페이징처리 시작 -->
<ul class="pagination justify-content-center">
    <!-- 이전페이지 -->
    <li class="page-item {$page <= 1 && 'disabled'}">
        <button class="page-link" on:click="{() => get_faq_list($page-1)}">이전</button>
    </li>
    
    <!-- 페이지번호 -->
    {#each Array(total_page) as _, loop_page}
    {#if loop_page >= $page-5 && loop_page <= $page+5}
    <li class="page-item {loop_page+1 === $page && 'active'}">
        <button on:click="{() => get_faq_list(loop_page+1)}" class="page-link">{loop_page+1}</button>
    </li>
    {/if}
    {/each}
    
    <!-- 다음페이지 -->
    <li class="page-item {$page > total_page-1 && 'disabled'}">
        <button class="page-link" on:click="{() => get_faq_list($page+1)}">다음</button>
    </li>
</ul>
<!-- 페이징처리 끝 -->