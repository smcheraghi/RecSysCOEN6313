<template>
  <div class="home">
    <Goods/>
  </div>
</template>

<script>
// @ is an alias to /src
import Goods from '@/components/Goods.vue'

export default {
  name: 'Home',
  components: {
    Goods
  }
}
</script>
