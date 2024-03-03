<script setup lang="ts">
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const loadingUsers = ref(true)
const loadingFoodAmount = ref(true)
const loadingBusinesses = ref(true)
const users = ref({})
const foodAmount = ref({})
const businesses = ref({})

const filtered = (time) => {
    const finalList = []
    for (const [key, item] of Object.entries(users.value)) {
        if (item.time === time) {
            finalList.push(item)
        }
    }
    return finalList
}

const numberOfMeals = (diet, time) => {
    let totalMeals = 0
    for (const [key, item] of Object.entries(users.value)) {
        if (item.diet === diet && item.time === time) {
            totalMeals += foodAmount.value[diet]
        }
    }
    return totalMeals
}

onMounted(async () => {
    await fetch('http://localhost:5001/getAllUsers', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        users.value = data
        loadingUsers.value = false
        console.log(data)
    })
    await fetch('http://localhost:5001/getFoodAmount')
    .then(response => response.json())
    .then(data => {
        foodAmount.value = data
        loadingFoodAmount.value = false
        console.log(data)
    })
    await fetch('http://localhost:5001/getAllBiz')
    .then(response => response.json())
    .then(data => {
        businesses.value = data
        loadingBusinesses.value = false
        console.log(data)
    })
})
</script>

<template>
    <h1 class="text-3xl font-bold">SurplusShare Dashboard</h1>
    <p class="mt-2 text-gray-500">View recipients and businesses, and initiate routes to drop off/pick up surplus.</p>

    <h2 class="mt-4 text-3xl font-semibold">📅 Today's summary</h2>
    <div class="my-4 flex">
        <div class="flex ml-4">
            <div v-if="loadingFoodAmount" class="px-9 py-6 bg-gray-200 animate-pulse rounded-md"></div>
            <h1 v-else class="text-6xl font-bold">{{ Object.values(foodAmount).reduce((a, b) => a + b, 0) }}</h1>
            <p class="mt-9 ml-1 text-sm">total meals</p>
        </div>
        <div class="ml-4 flex">
            <div v-if="loadingUsers" class="px-4 py-6 bg-gray-200 animate-pulse rounded-md"></div>
            <h1 v-else class="text-6xl font-bold">{{ Object.keys(users).length }}</h1>
            <p class="mt-9 ml-1 text-sm">recipients requesting food</p>
        </div>
        <div class="flex ml-4">
            <div v-if="loadingBusinesses" class="px-4 py-6 bg-gray-200 animate-pulse rounded-md"></div>
            <h1 v-else class="text-6xl font-bold">{{ Object.keys(businesses).length }}</h1>
            <p class="mt-9 ml-1 text-sm">businesses supplying food</p>
        </div>
    </div>

    <Tabs default-value="recipients" class="w-full">
        <TabsList class="w-full">
            <TabsTrigger class="w-1/2" value="recipients">
                Recipients
            </TabsTrigger>
            <TabsTrigger class="w-1/2" value="businesses">
                Businesses
            </TabsTrigger>
        </TabsList>
        <TabsContent value="recipients">
            <h3 class="mt-2 text-2xl font-semibold">🌅 5AM drop off</h3>
            <div v-if="loadingUsers || loadingFoodAmount" class="mt-2 bg-gray-200 w-full py-24 rounded-lg animate-pulse" />
            <div v-else>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead class="">
                            Name
                            </TableHead>
                            <TableHead>Address</TableHead>
                            <TableHead>Phone Number</TableHead>
                            <TableHead>Dietary Restrictions</TableHead>
                            <TableHead class="text-right">
                            Number of Meals
                            </TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        <TableRow v-for="user in filtered('5am')" :key="user">
                                <TableCell class="font-medium">
                                {{ user.name }}
                                </TableCell>
                                <TableCell>{{ user.address }}, {{ user.city}}</TableCell>
                                <TableCell>{{ user.phone }}</TableCell>
                                <TableCell>{{user.diet}}</TableCell>
                                <TableCell class="text-right">
                                {{ foodAmount[user.diet] }}
                                </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
                <div class="mt-4 mb-6">
                    <NuxtLink to="/dashboard/navigate?type=users&time=5am" class="px-6 py-2 bg-secondary rounded-lg text-white hover:bg-secondary/2">Navigate Drop Off Route</NuxtLink>
                </div>
            </div>
            <h3 class="mt-2 text-2xl font-semibold">⛅ 12PM drop off</h3>
            <div v-if="loadingUsers || loadingFoodAmount" class="mt-2 bg-gray-200 w-full py-24 rounded-lg animate-pulse" />
            <div v-else>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead class="">
                            Name
                            </TableHead>
                            <TableHead>Address</TableHead>
                            <TableHead>Phone Number</TableHead>
                            <TableHead>Dietary Restrictions</TableHead>
                            <TableHead class="text-right">
                            Number of Meals
                            </TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody class="mt-4">
                        <TableRow v-for="user in filtered('12pm')" :key="user">
                                <TableCell class="font-medium">
                                {{ user.name }}
                                </TableCell>
                                <TableCell>{{ user.address }}, {{ user.city}}</TableCell>
                                <TableCell>{{ user.phone }}</TableCell>
                                <TableCell>{{user.diet}}</TableCell>
                                <TableCell class="text-right">
                                    {{ foodAmount[user.diet] }}
                                </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
                <div class="mt-4 mb-6">
                    <NuxtLink to="/dashboard/navigate?type=users&time=12pm" class="mt-2 mb-4 px-6 py-2 bg-secondary rounded-lg text-white hover:bg-secondary/2">Navigate Drop Off Route</NuxtLink>
                </div>
            </div>
        </TabsContent>
        <TabsContent value="businesses">
            <div v-if="loadingBusinesses" class="mt-2 bg-gray-200 w-full py-24 rounded-lg animate-pulse" />
            <div v-else>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead class="">
                            Name
                            </TableHead>
                            <TableHead>Address</TableHead>
                            <TableHead>Phone Number</TableHead>
                            <TableHead>Type of Food</TableHead>
                            <TableHead>Amount of Food (~Meals)</TableHead>
                            <TableHead>Dietary Restrictions</TableHead>
                            <TableHead class="text-right">
                            Perferred Pick Up Time
                            </TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody class="mt-4">
                        <TableRow v-for="biz in businesses" :key="biz">
                                <TableCell class="font-medium">
                                {{ biz.name }}
                                </TableCell>
                                <TableCell>{{ biz.address }}, {{ biz.city}}</TableCell>
                                <TableCell>{{ biz.phone }}</TableCell>
                                <TableCell>{{ biz.foodType }}</TableCell>
                                <TableCell>{{ biz.foodAmount }}</TableCell>
                                <TableCell>{{biz.diet}}</TableCell>
                                <TableCell class="text-right">
                                    {{ biz.time }}
                                </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>
        </TabsContent>
    </Tabs>
</template>
