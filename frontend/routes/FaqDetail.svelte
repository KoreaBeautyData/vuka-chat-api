<script>
    import fastapi from "../src/lib/api"
    import { link, push } from 'svelte-spa-router'

    export let params = {}
    let faq_id = params.faq_id
    let faq = {}

    let question = ''
    let answer = ''

    function get_faq_detail() {
        fastapi("get", "/api/faq/" + faq_id, {}, (json) => {
            faq = json.result_data.faq
        })
    }
    get_faq_detail()
    
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
</script>

<div class="card">
  <h5 class="card-header">{faq.question}</h5>
  <div class="card-body">
    <p class="card-text">{faq.answer}</p>

    <a use:link href="/faq" class="btn btn-success" style="margin-top: 47px;">목록</a>
    <button class="btn btn-danger float-right m-2 mt-5" on:click={() => delete_faq_detail(faq.id)}>삭제</button>
    <a use:link href="/faq/modify/{faq.id}" class="btn btn-warning float-right m-2 mt-5">수정</a>
  </div>
</div>