<template>
  <div>
    <div>
      <p>Random number from backend: {{ randomNumber }}</p>
      <button @click="getRandom">New random number</button>
    </div>
    <hr>
    <div>
    <b-card-group deck v-for="item in commodity" v-bind:key="item.cid">
      <b-card title="title" img-src="" img-alt="Img" img-top>
            <p class="card-text">{{ item.price }}
              {{ item.title }}
              {{ item.categories }}
              {{ item.brand }}
              {{ item.imgUrl }}
              {{ item.salesRank }}
            </p>
            <div slot="footer">
                <small class="text-muted">Last updated 3 mins ago</small>
            </div>
      </b-card>
    </b-card-group>
    </div>
  </div>
</template>

<script>
import api from '@/config/api'

export default {
  data () {
    return {
      randomNumber: 0,
      commodity: [],
      error: ""
    }
  },
  created () {
    api().get('bestseller?start=2&limit=5').then(response => {
        this.commodity = response.data
    }).catch(error => {
      this.error = error
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
