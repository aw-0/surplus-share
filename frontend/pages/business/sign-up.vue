<script setup>
const name = ref('');
const address = ref('');
const city = ref('');
const phone = ref('');
const foodAmount = ref('');
const foodType = ref('');

const diet = ref('None');
const time = ref('5am');
const submit = async () => {
    console.log(name.value, address.value, city.value, phone.value, diet.value, time.value);
    await fetch('http://localhost:5001/registerBiz', {
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
            time: time.value,
            foodAmount: foodAmount.value,
            foodType: foodType.value
        })
    });
    await navigateTo('/sign-up-success');
}
</script>

<template>
    <h1 class="text-3xl font-bold">Sign up to donate</h1>
    <p class="mt-2 text-gray-500">Donate surplus food for your business to give back to the community.</p>
    
    <form class="mt-4 h-full">
        <h3 class="font-semibold">Business Name</h3>
        <input 
            type="text" 
            class="w-full mt-1 rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="Restaurant Name"
            v-model="name"
        >
        <br />
        <h3 class="mt-4 font-semibold">Street address</h3>
        <input 
            type="text" 
            class="w-full mt-1 rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="231 Surrey Lane"
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
        <h3 class="mt-4 font-semibold">Business Phone Number</h3>
        <input 
            type="tel" 
            class="w-full mt-1 rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="+18473451300"
            v-model="phone"
        >
        <br/>
        <h3 class="font-semibold mt-4">What type of food</h3>
        <input 
            type="number" 
            class="w-full mt-1 rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="Pizza, Sandwiches, etc."
            v-model="foodType"
        >
        <br/>
        <h3 class="font-semibold mt-4">How much food (estimated number of meals)</h3>
        <input 
            type="number" 
            class="w-full mt-1 rounded-lg border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            placeholder="3 meals"
            v-model="foodAmount"
        >
        <br/>
        <h3 class="font-semibold mt-4">Desired pick up time</h3>
        <select 
            class="block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-secondary focus:border-2 focus:ring-0 focus:ring-offset-0" 
            v-model="time"
        >
            <option selected>5am</option>
            <option>11pm</option>
        </select>
        <p class="text-sm text-gray-500">We will text you updates on the status of our drivers</p>
        <h3 class="font-semibold mt-4">Dietary Restrictions</h3>
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
        <button 
            class="mt-6 bg-secondary text-white w-full p-2 rounded-md hover:bg-secondary"
            @click="submit"
            type="button"
        >Sign up</button>
    </form>
</template>