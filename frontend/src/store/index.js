import { createStore } from "vuex";
import auth from "./modules/auth";

const store = createStore({
    modules: {
        auth,
    },
    state: {
        drawer: window.innerWidth > 1264,
    },
    mutations: {
        toggleDrawer(state) {
            state.drawer = !state.drawer;
        },
        setDrawer(state, value) {
            state.drawer = value;
        },
    },
});

export default store;
