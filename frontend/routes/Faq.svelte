<script>
    import { link } from 'svelte-spa-router'
    import fastapi from "../src/lib/api"

    let faq_list = [];
    let faq_count = 0;
    let page = 1;
    let page_length = 3;
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
            page = _page
            faq_count = json.result_data.faq_count
        })
    }
    get_faq_list(page);
</script>

<div class="col-4 m-3">
    <div class="input-group">
        <input type="text" class="form-control mr-3" bind:value="{kw}">
        <button class="btn btn-outline-secondary" on:click={() => get_faq_list(1)}>
            검색
        </button>
    </div>
</div>

{#each faq_list as faq}
<div class="card text-left bg-light mb-3s">
  <h5 class="card-header"><a use:link href="/faq/{faq.id}">{faq.question}</a></h5>
  <div class="card-body">
    <p class="card-text">{faq.answer}</p>
  </div>
</div>
{/each}


<!-- 페이징처리 시작 -->
<ul class="pagination justify-content-center">
    <!-- 이전페이지 -->
    <li class="page-item {page <= 1 && 'disabled'}">
        <button class="page-link" on:click="{() => get_faq_list(page-1)}">이전</button>
    </li>
    
    <!-- 페이지번호 -->
    {#each Array(total_page) as _, loop_page}
    {#if loop_page >= page-5 && loop_page <= page+5}
    <li class="page-item {loop_page+1 === page && 'active'}">
        <button on:click="{() => get_faq_list(loop_page+1)}" class="page-link">{loop_page+1}</button>
    </li>
    {/if}
    {/each}
    
    <!-- 다음페이지 -->
    <li class="page-item {page > total_page-1 && 'disabled'}">
        <button class="page-link" on:click="{() => get_faq_list(page+1)}">다음</button>
    </li>
</ul>
<!-- 페이징처리 끝 -->