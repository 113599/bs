import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import ViewUIPlus from 'view-ui-plus';
import 'view-ui-plus/dist/styles/viewuiplus.css';
import 'font-awesome/css/font-awesome.min.css';

import "./assets/style.css";

const app = createApp(App);
app.use(router);
app.use(store);
app.use(ViewUIPlus);

import initMenu from "./utils/menus.js";

router.beforeEach((to,from,next)=>{

  if(to.path == '/'){
    next();
  }else{
    if(store.state.menus != null){

        next();
    }else{

      initMenu(router, store);
      next();
    }
  }
});

app.mount('#app');
