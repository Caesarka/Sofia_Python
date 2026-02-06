

<template>
  <h2>Realty Page</h2>
  <p v-show="loading">Loading...</p>
  <template v-for="item in realty" :key="item.id">
    <SCard :title="item.title" :base-price="item.price" />
  </template>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SCard from '@/components/shared/SCard.vue';

const realty = ref([])
const isLoaded = ref(false)

async function getRealtyData () {
  isLoaded.value = false;

  try {
    const response = await fetch('/api/realty/');
    if (!response.ok) throw new Error('API error');

    realty.value = await response.json();
  } catch (e) {
    console.error(e);
  } 

  isLoaded.value = true;
}

onMounted(() => {
  getRealtyData();
});


</script>

<style>
.aaa {
  display: none;
}

.aaa1 {
  visibility: hidden;
}
</style>