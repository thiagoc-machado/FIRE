import { createStore } from 'vuex'
import auth from './modules/auth'

const store = createStore({
  modules: {
    auth
  },
  state: {
    drawer: true
  },
  mutations: {
    toggleDrawer(state) {
      state.drawer = !state.drawer
    }
  }
})

export default store
