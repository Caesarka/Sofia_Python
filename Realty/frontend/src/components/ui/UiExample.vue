<template>
  {{ value }}
  <input type="text" v-model="value">
</template>

<script setup>

const props = defineProps({
  example1: [Number, null]
})

const value = defineModel('example', { type: Number })
</script>