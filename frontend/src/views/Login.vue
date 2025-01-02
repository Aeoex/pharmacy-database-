<script>
import axios from 'axios';
export default{
  data(){
    return{
      username:'',
      password:''
    }
  },
  methods:{
    async validate(){
      // console.log(this.username, this.password);
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/token/', {
          username: this.username,
          password: this.password,
        });
        console.log(response);
        if (response.status === 200) {
          localStorage.setItem('access_token', response.data.access)
          this.$router.push("/about")
          
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.errorMessage = 'Invalid username or password.';
        } else {
          this.errorMessage = 'An error occurred. Please try again.';
        }
      }
      // if(this.password === "1"){
        // this.$router.push({name:'about'})
      }
      
    // }
  }
}
</script>

<template>
  <div class="container-fluid vh-100 bg-dark">
    <div class="row h-100 d-flex justify-content-center align-items-center">
      <div class="col-12 d-flex justify-content-center align-items-center">
        <div class="bg-dark h-100 w-50 p-3">
          <div class="d-flex justify-content-around align-items-center align-middle">
            <h3 class="mb-4">welcome</h3>
            <button class="btn btn-dark mb-3 btn-lg" v-on:click="this.$router.push('/signup')">sign up</button>
          </div>
          <form class="text-center">
            <div class="mb-3 d-flex justify-content-around align-items-center">
              <input type="text" class="form-control w-75 mb-3 d-flex justify-content-center" v-model="username" placeholder="username">
            </div>
            <div class="mb-3 d-flex justify-content-around align-items-center">
              <input type="password" class="form-control w-75" v-model="password" placeholder="password">
            </div>
            <div class="d-flex justify-content-center">
              <button type="submit" class="btn btn-secondary" @click.prevent="validate">submit
                <!-- <div class="spinner-border text-danger" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div> -->
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    </div>
    
    </template>
    
    <style scoped>
    *{
    color: aqua;
    }
    h3{
    font-size: xx-large;
    font:bold;
    }
    </style>