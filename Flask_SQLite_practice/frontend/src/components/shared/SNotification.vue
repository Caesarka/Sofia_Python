<template>
    <div>
        {{ description }}
    </div>
    <ui-button 
        :text="buttonProps.text" 
        :style="buttonProps.style" 
        />
</template>

<script setup>
import UiButton from '../ui/UiButton.vue';

defineProps({
    description: String,
    buttonProps: {
        type: Object,
        default: () => {
            return {
                text: "ok, got it!",
                style: {
                    color: "green"
                }
            }
        }
    }
});
</script>