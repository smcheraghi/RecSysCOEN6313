import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    commodities: []
  },
  mutations: {
    save(state, cid) {
      state.commodities.push(cid);
    },
  },
  actions: {
    save({
      commit
    }, cid) {
      commit("save", cid);
    },
  }
})
