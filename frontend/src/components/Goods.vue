<template>
  <div>
    <div class="commodities-list">
      <!-- <b-card-group deck class="mb-3"> -->
        <b-card class="commodity" v-for="item in commodity" v-bind:key="item.cid"
            :title=item.title
            :img-src=item.image_url
            img-alt="Image"
            img-top
            tag="article">
              <p class="card-text">
                {{ item.price }} CAD
              </p>
            <div class="text-center">
              <b-button variant="success" @click="addToCart(item.commodity_id)">Add</b-button>
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
      error: "",
      bottom: false,
      beers: [],
      startItem: -4
    }
  },
  watch: {
    bottom(bottom) {
      if (bottom) {
        this.addCommodities();
      }
    }
  },
  created () {
    window.addEventListener('scroll', () => {
      this.bottom = this.bottomVisible()
    })
    this.addCommodities()
  },
  methods: {
    addCommodities() {
      this.startItem += 6;
      let bestsellerQuery = 'bestseller?start=' + this.startItem + '&limit=6';
      api().get(bestsellerQuery).then(response => {
        this.commodity.push.apply(this.commodity, response.data);
        console.log(this.commodity);
      }).catch(error => {
        this.error = error
      })
    },
    bottomVisible() {
      const scrollY = window.scrollY
      const visible = document.documentElement.clientHeight
      const pageHeight = document.documentElement.scrollHeight
      const bottomOfPage = visible + scrollY >= pageHeight
      return bottomOfPage || pageHeight < visible
    },
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
      console.log("Adding to cart: ");
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