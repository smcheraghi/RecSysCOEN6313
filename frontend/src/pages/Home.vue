<template>
  <div>
    <p>Home page</P>
    <hr>
    <Random/>
  </div>
</template>

<script>
// @ is an alias to /src
import Random from '@/components/Random.vue'
export default {
  name: 'Home',
  components: {
    Random
  }
}
</script>
