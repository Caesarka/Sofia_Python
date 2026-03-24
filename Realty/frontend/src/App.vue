
<template>
  <h1>You did it!</h1>
  <div>
    <router-link to='/'>Home</router-link> | 
    <router-link :to="{ name: 'first'}">First page</router-link> | 
    <router-link :to="{ name: 'second'}">Second page</router-link> |
    <router-link :to="{ name: 'realty'}">Realty page</router-link> | 
    <router-link :to="{ name: 'realty_list'}">Realty list page</router-link>
  </div>
  <router-view />
</template>

<script setup>


</script>
