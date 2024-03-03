<script setup lang="ts">
const { time, type } = useRoute().query

onMounted(async() => {
    await fetch('http://localhost:5001/getUsersRoute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            time: '12pm'
        })
    })
})
</script>

<template>
    <h1 class="text-4xl font-bold">📍 Navigating to {{ type === 'users' ? 'recipients' : 'businesses' }} for {{ String(time).toUpperCase() }}</h1>
    <h2 class="mt-4 text-2xl">Your route:</h2>
    <ul class="mt-2 text-gray-600 ">
        <li>1. 123432423 Ln for Andrew Wolf</li>
    </ul>
</template>