<template>
    <div class="flex">
        <div class="my-auto">
            <p class="my-auto rounded-md font-bold text-4xl">
                Help Those in Need Today
            </p>
            <div class="ml-4 flex">
                <button class="mt-4 bg-secondary text-white rounded-md px-6 py-3 text-xl">
                    <NuxtLink to="/in-need/sign-up">
                        Request Help
                    </NuxtLink>
                </button>
                <button class="ml-2 mt-4 bg-secondary text-white rounded-md px-6 py-3 text-xl">
                    <NuxtLink to="/business/sign-up">
                        Donate Food
                    </NuxtLink>
                </button>
            </div>
        </div>
        <img class="ml-6 rounded-lg" src="/aadi-graphic.png" />
    </div>
    <p class="rounded-md text-large mt-4">
        Our Mission is to help those in need by connecting them to businesses with excess food.
    </p>


</template>