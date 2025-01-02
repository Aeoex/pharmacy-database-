<script>
import axios from 'axios';
const token = localStorage.getItem('access_token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
}
axios.defaults.withCredentials = true;
export default{
  data(){
    return{
      text:[],
      basket:[],
      quantity:0,
    }
  },
  async created(){
        const response = await axios.get('http://127.0.0.1:8000/api/drug/',{
          headers:`${token}`
        });
        // const data = await response.json()
        // console.log(data);
        console.log(response.data);
        if (response.status === 200) {
          this.text = response.data
          console.log(this.text);
          
        }        
  },
  methods:{
    async buy(x){
      console.log(x);
      
      if (x.quantity > 0) {
        const existingItem = this.basket.find((z) => z.name === x.name);
        if (existingItem) {
          existingItem.quantity += x.quantity;
          console.log(this.basket);
        } else {
          this.basket.push({ ...x });
          console.log(this.basket);
        }
      }
      
      try {
        const url = `http://127.0.0.1:8000/api/cart/add/${x.id}/${1}/${x.quantity}/`;
        
        const response = await axios.get(url);
        
        console.log(response.data.message);
        
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.error || 'An error occurred';
        } else {
          this.errorMessage = 'Failed to connect to the server.';
        }
      }
    },
    async buyall(){
      try {
        const url = `http://127.0.0.1:8000/api/cart/checkout/`;
        
        const response = await axios.post(url,{
          headers:`${token}`
        });
        
        console.log(response);
        this.basket=[]
        
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.error || 'An error occurred';
        } else {
          this.errorMessage = 'Failed to connect to the server.';
        }
      }
      const response = await axios.get('http://127.0.0.1:8000/api/drug/',{
          headers:`${token}`
        });
        // const data = await response.json()
        // console.log(data);
        console.log(response.data);
        if (response.status === 200) {
          this.text = response.data
          console.log(this.text);
          
        }      
    },
    async del(){
      this.basket = []
      try {
        const url = `http://127.0.0.1:8000/api/cart/clear/`;
        
        const response = await axios.get(url);
        
        console.log(response);
        
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.error || 'An error occurred';
        } else {
          this.errorMessage = 'Failed to connect to the server.';
        }
      }
    }
  }
}
</script>
<template>
  <div class="container-fluid vh-100">
    <div class="row vh-100">
      <div :class="`col-4 ${basket.length>0? `bg-info`:`bg-dark`} h-100 position-relative`">
        <h1 class="m-3" v-if="basket.length>0">basket</h1>
        <div class="scroll h-25 mt-5">
          <table class="table table-striped table-dark" v-if="basket.length > 0">
            <thead>
              <tr>
                <th scope="col" class="text-center align-middle">drug</th>
                <th scope="col" class="text-center align-middle">quantity</th>
                <th scope="col"></th>
                <th scope="col" class="align-middle"><button v-on:click="del()" class="btn btn-danger">delete</button></th>
              </tr>
            </thead>
            <tbody v-for="z in basket">
              <tr>
                <td class="text-center">{{z.name}}</td>
                <td class="text-center">{{ z.quantity }}</td>
                <td></td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="d-flex justify-content-center position-absolute bottom-50 start-50">
          <button class="btn btn-primary btn-lg" v-if="basket.length>0" v-on:click="buyall">buy</button>
        </div>
      </div>
      <div class="col-8 bg-danger h-100 scroll">
        <div class="row bg-dark scroll h-100">
          <h1 class="m-3 text-white">drugs</h1>
          <div class="col-4 d-flex justify-content-center" v-for="x in text">
            <div class="card mt-5" style="width: 25rem;">
              <img class="card-img-top" src="../assets/logo.svg" alt="Card image cap">
              <div class="card-body">
                <h5 class="card-title">{{ x.name }}</h5>
                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                <div class="d-flex justify-content-around">  
                  <input type="number" class="form-control w-25" v-model.number="x.quantity">
                  <button type="submit" v-on:click="buy(x)" class="btn btn-primary" v-if="x.quantity>0">add to basket</button>
                  <h3 class="text-end text-danger" v-else>sold out</h3>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.container-flui {
  height: 100%; /* Ensures the container fills the viewport height */
}
*{
  font-family: Tahoma, sans-serif;
}
h1{
  font-family: 'Courier New', monospace;
  font-weight: 900;
}
.scroll{
  overflow: scroll;;
}
.input{
  width: 70%;
  background-color: aqua;
  color: brown;
}

</style>
