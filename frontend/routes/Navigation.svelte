<script>
    import { link } from 'svelte-spa-router'
    import { page } from "../src/lib/store"
</script>

<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom mb=5">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/faq" on:click="{() => {$page = 0}}">FAQ</a>
        <a use:link class="navbar-brand" href="/tuning">Tuning</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContsent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" />
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a use:link class="nav-link" href="/chat">챗봇 Beta</a>
                </li>
            </ul>
        </div>
    </div>
</nav>