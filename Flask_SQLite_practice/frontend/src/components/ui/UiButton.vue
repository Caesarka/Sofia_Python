<template>
    <button :style="style"> {{ text }}</button>
</template>

<script setup>
defineProps({
    text: {
        type: String,
        required: true,
    },
    style: {
        type: [Object, String],
        default: "color: red;"
    }
});
</script>