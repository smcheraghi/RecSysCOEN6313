<template>
  <div class="cart">
    <CartView/>
  </div>
</template>

<script>
import CartView from '@/components/CartView.vue'

export default {
  name: 'Cart',
  components: {
    CartView
  }
}
</script>
