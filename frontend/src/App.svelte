<script>
  import Router from 'svelte-spa-router'
  import Faq from "../routes/Faq.svelte"
  import Chat from "../routes/Chat.svelte"
  import Navigation from "../routes/Navigation.svelte"

  const routes = {
    "/": Faq,
    "/chat": Chat,
  }
</script>

<Navigation />
<Router {routes}/>

