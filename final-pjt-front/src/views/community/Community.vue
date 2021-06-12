<template>
  <div class="font-neodgm">
    <div class="d-flex flex-column align-items-center">
      <img src="@/assets/globe.png" width="200px">
      <h1 class="my-3">Review 게시판</h1>
      <button @click="onClick">리뷰작성</button>
    </div>
    <hr>
    <div class="container d-flex">
      <table style="text-align:center;" class="fs-5">
        <thead>
          <tr>
            <th>리뷰 제목</th>
            <th>영화 </th>
            <th>작성일</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="review in reviews" :key="review.id" @click="getReview(review.id)" :review="review">
            <td>{{ review.title }}</td>
            <td>{{ review.movie_title }}</td>
            <td>{{ review.created_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name:'Community',

  data(){
    return {
      reviews:'',
      // titleList:[],
    }
  },
  props:{
    movieList:{
      type:Array,
    },
    isLogin:{
      type:Boolean
    }
  },
  methods:{
    onClick(){
      if (!this.isLogin){
        alert('Login이 필요합니다!')
        this.$router.push({name:'Login'})
      }else{
        this.$router.push({ name:'ReviewCreate'} )
      }
    },
    getReview(reviewId){
      console.log(reviewId)
      this.$router.push({ name:'ReviewDetail', params:{ reviewId:reviewId }})
    },
  },
  created(){
    axios({
      url:'http://127.0.0.1:8000/memovies/community',
      method:'get',
    })
      .then(res=>{
        this.reviews = (res.data)
        // console.log(this.reviews)

      })
      .catch(err=>{
        console.log(err)
      })
  }
}
</script>

<style>
table {
  border: 2px solid black;
  border-radius: 3px;
  background-color: #fff;
  width: 100%;
}

th{
  background-color:navy;
  color:white;
  border: 2px solid black;
  border-radius: 3px;
}

tr{
  border: 2px solid black;
  border-radius: 3px;
}

tbody{
  background-color: lightgrey;
  border: 2px solid black;
  border-radius: 3px;
}

td{
  border: 2px solid black;
  border-radius: 3px;
}

.font{
  font-family: 'Noto Sans KR', sans-serif;
}

h1{
  color: white;
}

</style>