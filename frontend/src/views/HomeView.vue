<template>
    <h2>Home View</h2>
    <!-- <h3> {{ msg }}</h3> -->
     <button @click="hello()"> click me</button>
    <div>
        <RouterLink to="/login">Login</RouterLink>
    </div>

    <div>
        <RouterLink to="/signup">signup</RouterLink>
    </div>
</template>



<script>
import axios from 'axios';

export default {
    data() {
        return {
            msg: "",
        };
    },

    methods:{
        async hello(){
            const token = localStorage.getItem('token')

            const response = await axios.get('http://localhost:5000/hello',
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );
            console.log(response)
            alert(response.data.msg)

        }
    },

    mounted() {
        this.hello()
    },
}

    </script>


<style scoped>



</style>
