<script setup lang="ts">
const { time, type } = useRoute().query

const stops = ref([])
const itemInfo = ref({})
const mapDirections = ref('')
const link = ref('')
const currentStop = ref(0)

const loading = ref(true)

onMounted(async() => {
    await fetch('http://localhost:5001/getUsersRoute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            time
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        stops.value = data.addresses
        itemInfo.value = data.users
        link.value = data.link
        
        let mapStr = '&origin=' + stops.value[0] + '&waypoints='
        stops.value.forEach((stop, index) => {
            if (index != 0 && index != stops.value.length - 1) {
                console.log(index)
                console.log(stops.value.length - 1)
                mapStr += stop + (index !== stops.value.length - 2 ? '|' : '')
            }
        })
        mapStr += '&destination=' + stops.value.at(-1)
        mapDirections.value = mapStr.replaceAll(' ', '+')
        loading.value = false
    })
})

const openLink = () => {
    window.open(link.value)
}

const setCurrentStop = () => {
    currentStop.value += 1
}

const returnToDash = () => {
    window.location.href = '/dashboard'
}
</script>

<template>
    <div v-if="currentStop == 0">
        <h1 class="text-4xl font-bold">📍 Navigating to {{ String(time).toUpperCase() }} {{ type === 'users' ? 'recipients' : 'businesses' }}</h1>
        <div class="flex w-full" v-if="!loading">
            <div class="relative w-1/2">
                <h2 class="mt-4 text-2xl">Your route:</h2>
                <div v-if="!loading">
                <ul class="mt-2 text-gray-700 text-xl">
                    <li v-for="(stop, index) in stops">{{ index + 1 }}. <b>{{ stop }}</b> for <b>{{ (Object.values(itemInfo).find((i) => (i.address + ', ' + i.city) === stop) ?? {name: 'Home Base'}).name }}</b></li>
                </ul>
                <div class="absolute bottom-0">
                    <button class="bg-primary text-white rounded-lg px-6 py-2" @click="openLink">Open in Google Maps</button>
                    <button class="bg-secondary text-white rounded-lg px-6 py-2 ml-2" @click="setCurrentStop()">Proceed to next stop</button>
                </div>
                </div>
            </div>
            <div class="w-1/2">
                <h2 class="mt-4 text-2xl">Map:</h2>
                <div v-if="!loading" class="h-96">
                    <iframe
                        referrerpolicy="no-referrer-when-downgrade"
                        class="rounded-lg w-full h-full"
                        :src="`https://www.google.com/maps/embed/v1/directions?key=AIzaSyCRjohDPZ0D83rNb2Nh2N8VGNgJXKBdenM${mapDirections}`"
                        allowfullscreen
                    />
                </div>
            </div>
        </div>
        <div class="flex flex-col mt-8 justify-center items-center" v-else>
            <h1 class="text-4xl font-semibold animate-bounce">Loading...</h1>
        </div>
    </div>
    <div v-else>
        <h1 class="text-4xl font-bold">📍 Navigating to {{ Object.values(itemInfo).find((i) => (i.address + ', ' + i.city) === stops[currentStop]).name }}</h1>
        <div class="flex w-full">
            <div class="relative w-1/2">
                <div class="h-full">
                    <h2 class="mt-4 text-2xl">Next address:</h2>  
                    <div class="grid h-3/4 place-items-center">              
                        <h2 class="text-4xl p-2 rounded-md bg-gray-300">{{ stops[currentStop] }}</h2>
                    </div>
                </div>
                <div class="absolute bottom-0">
                    <button class="bg-primary text-white rounded-lg p-2" @click="openLink">Open in Google Maps</button>
                    <button type="button" class="bg-secondary text-white rounded-lg p-2 ml-2" @click="(stops.length - 1 != currentStop) ? setCurrentStop() : returnToDash()">{{ (stops.length - 1 != currentStop) ? `Proceed to next stop` : `Back to Dashboard` }}</button>
                </div>
            </div>
            <div class="w-1/2">
                <h2 class="mt-4 text-2xl">Street View:</h2>
                <div class="h-96">
                    <iframe
                        class="rounded-lg w-full h-full"
                        referrerpolicy="no-referrer-when-downgrade"
                        :src="`https://www.google.com/maps/embed/v1/streetview?key=AIzaSyCRjohDPZ0D83rNb2Nh2N8VGNgJXKBdenM&location=${Object.values(itemInfo).find((i) => (i.address + ', ' + i.city) === stops[currentStop]).longlat.lat + ',' + Object.values(itemInfo).find((i) => (i.address + ', ' + i.city) === stops[currentStop]).longlat.lng}&fov=50`"
                        allowfullscreen
                    />
                </div>
            </div>
        </div>
    </div>
</template>