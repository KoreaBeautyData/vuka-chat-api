<script>
  import Router from 'svelte-spa-router'
  import Faq from "../routes/Faq.svelte"
  import FaqDetailCreate from "../routes/FaqDetailCreate.svelte"
  import FaqDetail from "../routes/FaqDetail.svelte"
  import FaqDetailModify from "../routes/FaqDetailModify.svelte"
  import Chat from "../routes/Chat.svelte"
  import ChatDB from "../routes/ChatDB.svelte"
  import Tuning from "../routes/Tuning.svelte"
  import TuningDetail from "../routes/TuningDetail.svelte"
  import Navigation from "../routes/Navigation.svelte"

  const routes = {
    "/faq": Faq,
    "/faq/create": FaqDetailCreate,
    "/faq/:faq_id": FaqDetail,
    "/faq/modify/:faq_id": FaqDetailModify,
    "/chat": Chat,
    "/chat/db": ChatDB,
    "/tuning": Tuning,
    "/tuning/:fine_tune_id": TuningDetail,
  }
</script>

<Navigation />
<Router {routes}/>

