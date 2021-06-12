<template>
  <div class="font-neodgm container p-0 mt-5" id="bigbox">
    <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">리뷰 수정</p>
      <span><img src="@/assets/update.png" width="20px" class="ms-2"></span>
    </div>
    <div class="d-flex flex-column align-items-center">
      <h1 style="color:black;" class="mb-2">게시글작성</h1>
      <form @submit.prevent="UpdateReview(review.id)" style="color:black;">
        <label for="title">리뷰 제목: </label>
        <input type="text" v-model="title" class="ms-1" style="width:400px">
        <br>
        <label for="movie_title" class="ms-5 my-1">영화: </label>
        <select class="ms-1" name="movie_title" @change="getInfo" :movie_title = "movie_title" style="width:400px">
          <option value="default" selected>{{movie_title}}</option>
        </select>
        <br>
        <label for="content">리뷰 내용: </label>
        <textarea class="ms-1" type="text" cols="30" rows="10" v-model="content" style="width:400px; vertical-align:top;"></textarea>
        <br>
        <button class="my-3" style="margin-left:230px;">리뷰 작성</button>
      </form>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import jwt_decode from 'jwt-decode'
export default {
  name:'ReviewUpdate',
  data(){
    return{
      review:[],
      nowUser:'',
      title:'',
      content:'',
      movie_title:'',
    }
  },
  props:{
    isLogin:{
      type:Boolean,
    }
  },
  created(){
    axios({
      url:`http://127.0.0.1:8000/memovies/community/reviews/`+this.$route.params.reviewid,
      method:'get',
    })
      .then(res=>{
        // console.log(res.data)
        this.review = res.data
        this.title = res.data.title
        this.movie_title = res.data.movie_title
        this.content = res.data.content
        if (this.isLogin) {
          this.nowUser = jwt_decode(localStorage.getItem('jwt')).user_id
        }
      })
  },
  methods:{
    UpdateReview(reviewId){
      axios({
          url:`http://127.0.0.1:8000/memovies/community/reviews/`+reviewId+'/change/',
          method:'put',
          data:{
            title:this.title,
            content: this.content,
            movie_title : this.movie_title,
            user : this.nowUser
          },
          headers: {
            Authorization: `JWT ${localStorage.getItem('jwt')}`,
          }
    })
      .then(res=>{
        console.log(res)
        this.$router.push({ name:'ReviewDetail', params:{reviewId:reviewId}})
      })
      .catch(err=>{
        console.log(err)
      })
    },
    getInfo(event){
      console.log(event.target)
      this.movie_title = event.target.value
    }
  },
}
</script>

<style>

</style>