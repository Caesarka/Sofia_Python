<template>
    <div data-xx='myCardDiv'>
        <h3>{{ title }}</h3>
        <p class="price--base price--old" v-if="discount !== 1">{{ basePrice }}</p>
        <p :class="priceClass">{{ basePrice * discount }}</p>
    </div>
    
</template>

<script setup>
import { computed } from 'vue';

const props2 = defineProps({
    title: {
        default: "title",
    },
    basePrice: {
        default: 100,
    },
    discount: {
        type: Number,
        default: 1
    }
});

const priceClass = computed(() => {
    if (props2.discount !== 1) {
        return "price--base"
    }
    return "price--discount"
})

</script>

<style scoped>
.price--base {
    color: black;
    font-size: 14px;
}

.price--old {
    text-decoration: line-through;
}

.price--discount {
    color: red;
    font-size: 22px;
    font-weight: bold;
}
</style>