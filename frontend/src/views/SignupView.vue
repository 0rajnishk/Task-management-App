<template>
    <h2>Signup Page</h2>

    <form @submit.prevent="signup">
        <div>
            <label for="username">Username</label>
            <input type="text" id="username" v-model="username" required />
        </div>
        <div>
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required />
        </div>
        <div>
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Sign Up</button>
    </form>
 
    <div>
        <RouterLink to="/">Home</RouterLink>
    </div>
    <div>
        <RouterLink to="/signup">Signup</RouterLink>
    </div>
</template>

<script>
import axios from 'axios'; 

export default {
    data() {
        return {
            username: "",
            email: "",
            password: "",
        };
    },

    methods: {
        async signup() {

            if (!this.username || !this.email || !this.password) {
                alert("All fields are required!");
                return;
            }
            
            const data = {
                username: this.username,
                email: this.email,
                password: this.password
            };

            try {
                const response = await axios.post('http://localhost:5000/signup', data);
                alert(response.data.message || 'Signup successful');
                
            } catch (error) {
                console.error("Signup Error:", error);


                if (error.response) {
                    alert(error.response.data.message || 'Signup failed');
                } else {
                    alert('Error during signup! Check your connection.');
                }
            }
        }
    }
}
</script>
