<template>
    <div>
        <h1 v-bind:title="tips">{{ msg }}</h1>
        <input type="text" v-model="msg"/>
        
    </div>
</template>

<script>
export default {
    setup() {
        
    },
    data() {
        return {
            msg: 'Hello World',
            tips: 'This is a header'
        }
    }
}
</script>

<style scoped>

</style>