<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../src/lib/api"

    let faq_id = '';
    let question = '';
    let answer = '';

    function post_faq(event) {
        event.preventDefault()

        let url = "/api/faq"
        let params = {
            question: question,
            answer: answer,
        }
        fastapi('post', url, params, (json) => {
                faq_id = json.id
                question = json.question
                answer = json.answer
                push("/faq/" + faq_id)
            }
        )
        console.log(faq_id);
        console.log(question);
        console.log(answer);
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
        <button class="btn btn-success float-right" on:click="{post_faq}">저장</button>
    </form>
</div>