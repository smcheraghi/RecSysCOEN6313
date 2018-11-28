<template>
  <div>
    <div>
      <div class="commodities-list">
      <!-- <b-card-group deck class="mb-3"> -->
        <b-container class="bv-example-row" v-for="item in goods" v-bind:key="item.commodity_id">
          <b-row>
              <b-col><img :src=item.image_url></b-col>
              <b-col>
                <br>
                {{ item.title }}
                <br>
                <br>
                {{ item.price }} CAD
                <br>
                <a @click="removeItem(item.commodity_id)">
                  Remove
                </a>
              </b-col>
          </b-row>
        </b-container>
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
  watch: {
  },
  created() {
    this.commodities = this.$store.state.commodities;
    for (let i=0; i<this.commodities.length; i++) {
      let query = '/commodity/' + this.commodities[i];
      console.log(query);
      api().get(query).then(response => {
        this.goods.push(response.data);
        console.log(this.goods);
    }).catch(error => {
      this.error = error
    });
    }
    // api().get('/commodity').then(response => {
    //     this.goods = response.data
    // }).catch(error => {
    //   this.error = error
    // });
    // console.log("Goods from API: " + this.goods);
    // this.commodities = this.$store.state.commodities;
    // //console.log("Goods in the cart: " + this.commodities);
    // let k =0;
    // for (let i=0; i<this.goods.length; i++) {
    //   for (let j=0; j<this.commodity.length; j++) {
    //     if(this.goods[i].cid === this.commodity[j]) {
    //       this.cart[k] = this.goods[i];
    //       k++;
    //     }
    //   }
    // }
    // this.goods = this.$store.state.commodities;
    // console.log("Goods: " + this.$store.state.commodities);
    // api().get('/commodity').then(response => {
    //     this.commodity = response.data
    // }).catch(error => {
    //   this.error = error
    // })
  },
  methods: {
    removeItem(cid) {
      for (let i=0; i<this.goods.length; i++) {
        if (this.goods[i].commodity_id == cid)
          console.log("delete");
      }
    }
  }
}
</script>

<style scoped>
.cart_item {
  margin-top: 10rem;
  height: 10rem;
  width: 20rem;
}
.bv-example-row {
  font-size: 16pt;
  border: 1px solid gray;
  padding: 2rem;
  margin-top: 2rem;
  width: 50rem;
}
.bv-example-row a {
  color: black !important;
  cursor: pointer;
  font-size: 14pt;
}
.bv-example-row a:hover {
  color: #007bff !important;
  cursor: pointer;
  font-size: 14pt;
}
</style>