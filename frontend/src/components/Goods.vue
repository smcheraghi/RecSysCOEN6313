<template>
  <div>
    <div>
      <p>Random number from backend: {{ randomNumber }}</p>
      <button @click="getRandom">New random number</button>
    </div>
    <hr>
    <div class="commodities-list">
      <!-- <b-card-group deck class="mb-3"> -->
        <b-card class="commodity" v-for="item in commodity" v-bind:key="item.cid"
            :title=item.title
            :img-src=item.imgUrl
            img-alt="Image"
            img-top
            tag="article">
              <p class="card-text">
                {{ item.price }} CAD
              </p>
            <div class="text-center">
              <b-button variant="success" @click="addToCart(item.cid)">Add</b-button>
            </div>
              <!-- <div slot="footer">
                  <small class="text-muted">Last updated 3 mins ago</small>
              </div> -->
        </b-card>
      <!-- </b-card-group> -->
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
    },
    addToCart(cid) {
      console.log("Adding to cart: " + cid);
      this.$store.commit("save", cid);
      console.log("Saved: " + this.$store.state.commodities);
    }
  }
}
</script>

<style>
.commodities-list {
  padding: 1rem 5rem 10rem 5rem;
}
.commodity {
  display: inline-block;
  width: 15rem;
  margin-left: 6rem;
  margin-top: 3rem;
}
</style>