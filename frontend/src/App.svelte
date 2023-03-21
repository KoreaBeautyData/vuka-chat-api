<script>
  import Router from 'svelte-spa-router'
  import Faq from "../routes/Faq.svelte"
  import FaqDetail from "../routes/FaqDetail.svelte"
  import FaqDetailModify from "../routes/FaqDetailModify.svelte"
  import Chat from "../routes/Chat.svelte"
  import Navigation from "../routes/Navigation.svelte"

  const routes = {
    "/faq": Faq,
    "/faq/:faq_id": FaqDetail,
    "/faq/modify/:faq_id": FaqDetailModify,
    "/chat": Chat,
  }
</script>

<Navigation />
<Router {routes}/>

