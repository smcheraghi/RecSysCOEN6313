<template>
  <div>
    <div>
      <p>Random number from backend: {{ randomNumber }}</p>
      <button @click="getRandom">New random number</button>
    </div>
    <hr>
    <div>
      {{ test }}
    </div>
  </div>
</template>

<script>
import api from '@/config/api'

export default {
  data () {
    return {
      randomNumber: 0,
      test: ""
    }
  },
  created () {
    api().get('/test')
      .then(response => {
        this.test = response.data
      })
  },
  methods: {
    getRandom () {
      this.randomNumber = this.getRandomFromBackend()
    },
    getRandomFromBackend () {
      api().get('random').then(response => {
        this.randomNumber = response.data.randomNumber
      }).catch(error => {
        // console.log(error)
        // Fixme
        this.randomNumber = error
      })
    }
  }
}
</script>
