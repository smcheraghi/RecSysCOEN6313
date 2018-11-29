<template>
  <div>
    <div class="commodities-list">
      <!-- <b-card-group deck class="mb-3"> -->
        <b-card class="commodity" v-for="item in commodity" v-bind:key="item.cid"
            :title=item.title
            img-alt="Image"
            img-top
            tag="article">
            <img :src=item.image_url @click="modalShow = !modalShow"/>
              <p class="card-text">
                {{ item.price }} CAD
              </p>
            <div class="text-center">
              <b-button variant="success" @click="addAction(item.commodity_id, 'info')">More Info</b-button>
            </div>
            <div class="text-center">
              <b-button variant="success" @click="addAction(item.commodity_id, 'cart')">Add</b-button>
            </div>
              <!-- <div slot="footer">
                  <small class="text-muted">Last updated 3 mins ago</small>
              </div> -->
        </b-card>
      <!-- </b-card-group> -->
    </div>
    <b-modal v-model="modalShow">
      <p class="my-4">Hello from modal!</p>
    </b-modal>
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
      startItem: -4,
      modalShow: false,
      recommendations: [],
      actions: [],
      currentChunk: 0
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
    addAction(cid, action) {
      this.actions.push(cid);
      if (action === 'cart') {
        this.addToCart(cid);
      }
      if ((this.actions.length % 3) === 0) {
        this.retrieveRecommendations();
      }
    },
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
    addToCart(cid) {
      this.$store.commit("save", cid);
    },
    async retrieveRecommendations() {
      let date = new Date();
      let timestamp = date.getTime();
      let actionArr = this.actions;
      console.log(actionArr);
      let result = await api().post("behavior", [{
        "reviewerID": 192500,
        "asin": actionArr[this.currentChunk],
        "unixReviewTime": timestamp
      },
      {
        "reviewerID": 192500,
        "asin": actionArr[this.currentChunk+1],
        "unixReviewTime":timestamp
      },
      {
        "reviewerID": 192500,
        "asin": actionArr[this.currentChunk+2],
        "unixReviewTime":timestamp
      }
      ]);
      this.recommendations = JSON.parse(result.data.recommendation);
      console.log("Rec: " + this.recommendations + this.recommendations.length);
      //console.log("Rec: " + JSON.parse(this.recommendations) + JSON.parse(this.recommendations).length);
      this.currentChunk += 3;
      this.addRecommendations();
    },
    addRecommendations() {
      for (let i=0; i< this.recommendations.length; i++) {
        let query = '/commodity/' + this.recommendations[i];
        console.log("Query: " + query);
        api().get(query).then(response => {
          console.log(response.data);
          this.commodity.push(response.data);
          console.log(this.commodity);
        }).catch(error => {
          this.error = error
        })
      }
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