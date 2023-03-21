<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../src/lib/api"

    export let params = {}
    const faq_id = params.faq_id

    let question = ''
    let answer = ''

    fastapi("get", "/api/faq/" + faq_id, {}, (json) => {
        question = json.result_data.faq.question
        answer = json.result_data.faq.answer
    })

    function put_faq_detail(event) {
        event.preventDefault()
        
        let url = "/api/faq/" + faq_id
        let params = {
            question: question,
            answer: answer,
        }
        fastapi('put', url, params, (json) => {
                push("/faq/"+faq_id)
            }
        )
    }
</script>

<div class="container">
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="question">Question</label>
            <input type="text" class="form-control" bind:value="{question}">
        </div>
        <div class="mb-3">
            <label for="answer">Answer</label>
            <textarea class="form-control" rows="10" bind:value="{answer}"></textarea>
        </div>
        <button class="btn btn-warning float-right" on:click="{put_faq_detail}">수정하기</button>
    </form>
</div>