
<template>
  <p>
    There is {{ example }} example variable.
    There is {{ example1 }} example variable.
  </p>
  <p>
    Sum {{ sum }}
  </p>
  <button @click="clickBtn">click</button>
  <button @click="clickBtnEx">ex1</button>
  <button @click="getResult">result</button>
  <div>
    <input v-model="example"/>
    <input v-model="example1" />
    
  </div>
</template>

<script setup>
import { ref } from 'vue';

let example = ref(1);
let example1 = ref(10);
let sum = ref();

const clickBtn = () => {
  example.value = Number(example.value) + 1;

  console.log(example);
}

const clickBtnEx = () => {
  example1.value = Number(example1.value) - 10;

  console.log(example1);
}

const getResult = () => {
  sum.value = Number(example.value) + Number(example1.value);
}


</script>
