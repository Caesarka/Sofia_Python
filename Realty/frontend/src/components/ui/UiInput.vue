<template>
    <div class='ui-input' :class="{'ui-input--error': hasError}">
        <label :for="name">{{ label }}</label>
        <input 
            v-model="modelValue"
            :id="name"
            :name="name"
            :placeholder="placeholder"
        />
        <p class="error-message" v-if="hasError">
            {{ error }}
        </p>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const modelValue = defineModel({ type: [String, Number, null] });

const props = defineProps({
    label: {
        type: [String],
        default: "",
        required: true
    },
    placeholder: {
        type: [String],
        default: "label",
    },
    name: {
        type: String,
        required: true
    },
    error: {
        type: String,
        default: ""
    },
});

const hasError = computed(() => {
  return props.error.length;
});
</script>

<style lang='scss'>
.ui-input {
    &--error input{
        border-color: red;
    }

    .error-message {
        color: red;
    }
}
</style>