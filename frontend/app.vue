<script setup lang="ts">
import {
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu'
</script>

<template>
    <nav class="navbar flex">
        <div class="mr-4 ">
        <NuxtLink class="navbar-brand flex py-2 ml-2" to="/">
            <img src="/logo.png" alt="Logo" width="60" height="60" class="d-inline-block align-text-top">
            <p class="text-primary my-auto font-bold text-lg">SurplusShare</p>
        </NuxtLink>
        </div>
        <NavigationMenu>
            <NavigationMenuList>
                <NavigationMenuItem>
                    <NuxtLink to="/in-need/sign-up">
                        <NavigationMenuLink :class="navigationMenuTriggerStyle()">
                            For Individuals
                        </NavigationMenuLink>
                    </NuxtLink>
                </NavigationMenuItem>
                <NavigationMenuItem>
                    <NuxtLink to="/business/sign-up">
                        <NavigationMenuLink :class="navigationMenuTriggerStyle()">
                            For Businesses
                        </NavigationMenuLink>
                    </NuxtLink>
                </NavigationMenuItem>
                <NavigationMenuItem class="justify-end">
                    <NuxtLink to="/dashboard">
                        <NavigationMenuLink :class="navigationMenuTriggerStyle()">
                            For Volunteers
                        </NavigationMenuLink>
                    </NuxtLink>
                </NavigationMenuItem>
            </NavigationMenuList>
        </NavigationMenu>
    </nav>
    <div class="bg-secondary h-screen max-h-max px-24 py-12">
        <div class="bg-white p-6 rounded-md">
            <NuxtPage />
        </div>
    </div>
</template>
