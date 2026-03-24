<template>
  <p>Hello</p>
  <ul>
    <li v-for="(color, index) in a" :key="index">
      {{ color }}
    </li>
  </ul>

  <div 
    v-for='color in b'
    :style="{
      width: '100px',
      height: '100px',
      backgroundColor: color.hex,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }"
    :key='color.name'
  >
    {{ color.name }}
  </div>
</template>

<script setup>
const a = [
  'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'
]

const b = [
  {
    name: 'red',
    hex: '#FF0000'
  },
  {
    name: 'orange',
    hex: '#FFA500'
  },
  {
    name: 'yellow',
    hex: '#FFFF00'
  },
  {
    name: 'green',
    hex: '#008000'
  },
  {
    name: 'blue',
    hex: '#0000FF'
  },
  {
    name: 'indigo',
    hex: '#4B0082'
  },
  {
    name: 'violet',
    hex: '#EE82EE'
  }
]
  </script>