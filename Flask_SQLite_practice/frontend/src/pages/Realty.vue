<template>
  <h2>Realty Page</h2>
  <p v-if="loading">Loading...</p>
  <ul v-else>
    <li v-for="item in realty" :key="item.id">
      <p>{{item.id}}</p>
      {{ item.id }}
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const realty = ref([])
const loading = ref(true)

onMounted(async () => {
  const response = await fetch('/api/realty/1')
  console.log('response', response)
  
  realty.value = await response.json()
  console.log('realty', realty.value)
  loading.value = false
})
</script>