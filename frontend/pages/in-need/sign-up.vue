<script setup>
const name = ref('');
const address = ref('');
const city = ref('');
const phone = ref('');
const diet = ref('None');
const time = ref('5am');
const submit = async () => {
    console.log(name.value, address.value, city.value, phone.value, diet.value, time.value);
    await fetch('http://localhost:5001/registerUser', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name.value,
            address: address.value,
            city: city.value,
            phone: phone.value,
            diet: diet.value,
            time: time.value
        })
    });
    await navigateTo('/sign-up-success');
}
</script>


<template>
    <h1 class="text-3xl font-bold">Sign up for assistance</h1>
    <p class="mt-2 text-gray-500">We'll connect you to local business with surplus, day-old food. Get them delivered directly to your home.</p>

    <form class="mt-4 h-full">
        <h3 class="font-semibold">Full name</h3>
        <input 
            type="text" 
            class="w-full rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="John Smith"
            v-model="name"
        >
        <br />
        <h3 class="mt-4 font-semibold">Street address</h3>
        <input 
            type="text" 
            class="w-full rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="123 Main Street"
            v-model="address"
        >
        <br/>
        <h3 class="mt-4 font-semibold">City</h3>
        <input 
            type="text" 
            class="w-full mt-1 rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="Lincolnshire"
            v-model="city"
        >
        <br/>
        <h3 class="mt-4 font-semibold">Phone number</h3>
        <input 
            type="text" 
            class="w-full mt-1 rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="+18473232526"
            v-model="phone"
        >
        <p class="text-gray-500 text-xs mt-1 ml-1">We'll text you updates daily on the status of your food</p>
        <br />
        <h3 class="font-semibold">Dietary Restrictions</h3>
        <select 
            class="block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            v-model="diet"
        >
            <option selected>None</option>
            <option>Vegetarian/Vegan</option>
            <option>Gluten Free</option>
            <option>Halal</option>
            <option>Kosher</option>
        </select>
        <br />
        <h3 class="font-semibold">Perferred Drop Off Time</h3>
        <select 
            class="block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            v-model="time"
        >
            <option selected>5am</option>
            <option>12pm</option>
        </select>
        <button 
            class="mt-6 bg-secondary text-white w-full p-2 rounded-md hover:bg-gray-800 transition-all duration-200 hover:rounded-xl hover:shadow-xl"
            @click="submit"
            type="button"
        >Sign up</button>
    </form>
</template>
