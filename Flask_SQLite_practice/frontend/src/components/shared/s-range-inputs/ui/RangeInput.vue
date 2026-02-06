<template>
  <ui-input 
    v-model="minInputValue" 
    :label="labelInputs.minLabel" 
    :error="minError"
    name='minValue'
  />
  <ui-input 
    v-model="maxInputValue" 
    :label="labelInputs.maxLabel"
    :error="maxError"
    name='maxValue'

  />
  <p class="error-message" v-if="rangeErrorMessage">
    {{ rangeErrorMessage }}
  </p>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import UiInput from '@/components/ui/UiInput.vue';

const props = defineProps({
    labelInputs: {
        type: [Object],
        default: () => {
          return { 
            minLabel: 'Min',
            maxLabel: 'Max',
          }
        },
    },
    placeholder: {
        type: [Object],
        default: () => {
          return { 
            minPlaceholder: 'Min',
            maxPlaceholder: 'Max',
          }
        },
    },
    // name: {
    //     type: String,
    //     required: true
    // },
    error: {
        type: String,
        default: ""
    },

    // Свойства не должны быть по названию такими же, как v-model значения!
    minDefaultValue: {
        type: [String, Number],
        default: 1
    },
    maxDefaultValue: {
        type:[String, Number],
        default: 100000000
    }
});

const emits = defineEmits(['call-error']);

// Добавить две ref переменные: для минимального и максимального значений. Заменить в вычислении ошибок. Передать в инпуты.

const minInputValue = defineModel('minValue', { type: [String, Number, null] });
const maxInputValue = defineModel('maxValue', { type: [String, Number, null] });

const minError = computed(() => {
  // проверка на число
  if (isNaN(minInputValue.value)) {
    return `Value must be a Number`;
  }
  
  // проверка на ограничение из свойств
  if (Number(minInputValue.value) < props.minDefaultValue) {
    return `Value must be at least ${props.minDefaultValue}`;
  }

  return;
});

const maxError = computed(() => {
  // проверка на число
  if (isNaN(maxInputValue.value)) {
    return `Value must be a Number`;
  }

    // проверка на ограничение из свойств
  if (Number(maxInputValue.value) > props.maxDefaultValue) {
    return `Value must be no more than ${props.maxDefaultValue}`;
  }

  return;
});

const rangeErrorMessage = computed(() => {
  // условие, что не может быть больше макс
  if (Number(minInputValue.value) > Number(maxInputValue.value)) {
    return `Min value cannot be greater than Max value`;
  }

  return;
});

watch([minError, maxError, rangeErrorMessage], (newValues) => {
  let findError = false;
  for (let e of newValues) {
    if (e) {
      findError = true
      break;
    }
  }
  
  emits('call-error', findError);
})
</script>

<style lang='scss'>
.error-message {
    color: red;
}
</style>
