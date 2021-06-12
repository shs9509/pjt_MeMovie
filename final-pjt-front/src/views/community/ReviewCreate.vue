<template>
  <div class="font-neodgm container p-0 mt-5" id="bigbox">
    <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">리뷰 작성</p>
      <span><img src="@/assets/write.png" width="20px" class="ms-2"></span>
    </div>
    <div class="d-flex flex-column align-items-center">
      <h1 style="color:black;" class="mb-2">게시글작성</h1>
      <form @submit.prevent="CreateReview" style="color:black;">
        <label for="title">리뷰 제목: </label>
        <input type="text" v-model="title" class="ms-1" style="width:400px">
        <br>
        <label for="movie_title" class="ms-5 my-1">영화: </label>
        <select class="ms-1" name="movie_title" @change="getInfo" :movie_title = "movie_title" style="width:400px">
          <option value="default">영화 선택</option>
          <option v-for="movie_title in titleList" :key="movie_title.id" >{{ movie_title }}</option>
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
import jwt_decode from "jwt-decode"

export default {
  name:'ReviewCreate',
  data(){
    return {
      title:'',
      content:'',
      movie_title:'',
      user:jwt_decode(localStorage.getItem('jwt')).user_id,
      titleList:[],
      movieList:[],
    }
  },
  props:{
    isLogin:{
      type:Boolean
    }
  },
  created(){
    axios({
      url:'http://127.0.0.1:8000/memovies/movies/',
      method:'get',
    })
      .then(res=>{
        this.movieList = res.data
        console.log(res.data)
        this.getTitles
        if (this.isLogin) {
          this.nowUser = jwt_decode(localStorage.getItem('jwt')).user_id
        }
      })
      .catch(err=>{
        console.log(err)
      })
  },
  methods:{
    CreateReview(){
      const userid = jwt_decode(localStorage.getItem('jwt')).user_id
      axios({
        url:'http://127.0.0.1:8000/memovies/community/reviews/',
        method:'post',
        headers: {
          Authorization: `JWT ${localStorage.getItem('jwt')}`,
        },
        data: {
          title: this.title,
          content: this.content,
          movie_title: this.movie_title,
          user: userid,
        }
      })
        .then(res=>{
          this.$router.push({ name:'Community'})
          console.log(res.data)
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
  computed:{
    getTitles(){
     this.movieList.tmdb.forEach(movie=>{
       this.titleList.push(movie.movie_title)
     })
     this.movieList.naver.forEach(movie=>{
       this.titleList.push(movie.movie_title)
     })
     this.movieList.boxoffice.forEach(movie=>{
       this.titleList.push(movie.movie_title)
     })
     return this.titleList
    },
  },
}
</script>

<style>
  #bigbox {
    background-color: lightgrey;
    border: 3px solid black;
  }
  #topbar{
    background-color:navy;
    height:30px
  }
</style>