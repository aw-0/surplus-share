<template>
    <div class="flex">
        <div class="my-auto mx-auto">
            <p class="my-auto rounded-md font-bold text-4xl text-gray-800">
                Help Those in Need Today
            </p>
            <p class="text-center mt-3 text-3xl font-bold text-gray-600">
                Sign up for Support
            </p>
            <div class="mx-auto text-center">
                <button class="mt-4 bg-secondary text-white rounded-md px-6 py-3 text-xl hover:bg-gray-800 transition-all duration-200 hover:rounded-xl hover:shadow-xl">
                    <NuxtLink to="/in-need/sign-up">
                        Request Help
                    </NuxtLink>
                </button>
                <button class="ml-2 mt-4 bg-secondary text-white rounded-md px-6 py-3 text-xl hover:bg-gray-800 transition-all duration-200 hover:rounded-xl hover:shadow-xl">
                    <NuxtLink to="/business/sign-up">
                        Donate Food
                    </NuxtLink>
                </button>
            </div>
        </div>
        <img class="mx-auto rounded-lg" src="/aadi-graphic.png" />
    </div>
    <div class="mt-6 flex flex-col items-center">
        <p class="text-2xl font-semibold">
            Our Mission is to help people by connecting them to businesses with excess food.
        </p>
    </div>


</template>