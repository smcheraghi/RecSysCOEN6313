<template>
  <div>
    <p>About page</P>
    <hr>
    <Ping/>
  </div>
</template>

<script>
// @ is an alias to /src
import Ping from '@/components/Ping.vue'
export default {
  name: 'About',
  components: {
    Ping
  }
}
</script>
