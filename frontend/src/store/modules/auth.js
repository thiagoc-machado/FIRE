import axios from '../../services/api'

const state = {
  accessToken: localStorage.getItem('accessToken') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  user: null
}

const mutations = {
  setTokens(state, { access, refresh }) {
    state.accessToken = access
    state.refreshToken = refresh
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)
  },
  clearTokens(state) {
    state.accessToken = null
    state.refreshToken = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  },
  setUser(state, user) {
    state.user = user
  }
}

const actions = {
  async login({ commit }, credentials) {
    const res = await axios.post('/api/auth/jwt/create/', credentials)
    commit('setTokens', res.data)
  },
  async fetchUser({ commit, state, dispatch }) {
    if (!state.accessToken) return

    try {
      // Verifica se o token ainda é válido
      await axios.post('/api/auth/jwt/verify/', {
        token: state.accessToken
      })

      // Se OK, busca dados do usuário
      const res = await axios.get('/api/auth/users/me/')
      commit('setUser', res.data)

    } catch (error) {
      // Token inválido ou expirado → logout forçado
      dispatch('logout')
    }
  },
  logout({ commit }) {
    commit('clearTokens')
    commit('setUser', null)
    window.location.href = '/login'
  },
}

const getters = {
  isAuthenticated: state => !!state.accessToken,
  getUser: state => state.user
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
