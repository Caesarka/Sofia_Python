<template>
    <div>
        <!-- <ui-input 
            v-for="item in formInputs"
            v-model="formValues[item.name]"
            :key="item.name"
            :label="item.label"
            :name="item.name"
            :placeholder="item.placeholder"
            :type="item.type"
            :error="rangeError"
        /> -->
        <s-range-input
            v-model:min-value="formValues.size_from"
            v-model:max-value="formValues.size_to"
            @callError="setError"
        />
        <ui-example v-model:example="exValue"></ui-example>
    </div>
    <button @click="send" :disabled="isError">send</button>
    <p v-if="isError">{{ isError }}</p>
    {{ formValues }}
</template>

<script setup>
import { ref,reactive, computed, } from 'vue';
import UiInput from '../ui/UiInput.vue'; // export default
import { SRangeInput } from './s-range-inputs'; // export { RangeInput }
import UiExample from '../ui/UiExample.vue';

const exValue = ref(1);

const formInputs = [
    {
        label: "Size",
        name: "size_from",
        placeholder: "Input the min size",
        type: 'number'
        
    },
    {
        label: "",
        name: "size_to",
        placeholder: "Input the max size",
        type: 'number'
    }
];

const formValues = reactive({
    size_from: null,
    size_to: null,
});

const isError = ref(false);

const setError = (v) => {
    isError.value = v;
}

function send() {
    fetch('/', {
        method: 'POST',
        body: JSON.stringify(formValues),
    })
};
</script>