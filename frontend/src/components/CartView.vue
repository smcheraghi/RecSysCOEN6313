<template>
  <div>
    <div>
      <div class="commodities-list">
      <!-- <b-card-group deck class="mb-3"> -->
        <b-card v-for="item in cart" v-bind:key="item.cid"
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
  </div>
</template>

<script>
import api from '@/config/api'

export default {
  data () {
    return{
      goods: [],
      commodities: [],
      cart: []
    }
  },
  created() {
    api().get('/commodity').then(response => {
        this.goods = response.data
    }).catch(error => {
      this.error = error
    });
    console.log("Goods from API: " + this.goods);
    this.commodities = this.$store.state.commodities;
    //console.log("Goods in the cart: " + this.commodities);
    let k =0;
    for (let i=0; i<this.goods.length; i++) {
      for (let j=0; j<this.commodity.length; j++) {
        if(this.goods[i].cid === this.commodity[j]) {
          this.cart[k] = this.goods[i];
          k++;
        }
      }
    }
    // this.goods = this.$store.state.commodities;
    // console.log("Goods: " + this.$store.state.commodities);
    // api().get('/commodity').then(response => {
    //     this.commodity = response.data
    // }).catch(error => {
    //   this.error = error
    // })
  }
}
</script>

<style>
</style>