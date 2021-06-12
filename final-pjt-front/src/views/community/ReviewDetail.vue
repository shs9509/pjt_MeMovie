<template>
<!-- 영화별 상세 정보 page -->
  <div class="font-neodgm">
    <div class="container mt-5 p-0 fs-5" id="bigbox">
      <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">{{ review.title }}</p>
      <span><img src="@/assets/update.png" width="20px" class="ms-2"></span>
      </div>
      <div class="d-flex flex-column align-items-center mx-5">
        <h4 style="color:black;">{{ review.title }}</h4>
        <p style="color:black;" class="mb-1">작성자 : <router-link :to="{ name:'Profile', params:{userid:review.user}}" style="text-decoration:none; color:navy;" v-text="review.username"></router-link></p>
        <p style="color:black;">작성일: {{ review.created_at }}</p>
        <p style="color:black;"><i class="fas fa-film"></i> {{ review.movie_title }}</p>
        <div style="color:black;">
          <p class="fs-5">{{ review.content }}</p>
        </div>
        <button v-if=" review.user === nowUser" class="btn btn-none" @click="reviewUpdate(review.id)"><img src="@/assets/update.png" width="30px">수정</button>
        <button v-if=" review.user === nowUser" class="btn btn-none" @click="reviewDelete(review.id)"><img src="@/assets/delete.png" width="30px">삭제</button>
      </div>
      </div>
    <div class="mt-4 container py-2 d-flex justify-content-center" id="comment">
      <form @submit.prevent="createComment">
        <label for="content" class="me-2">의견을 남겨주세요: </label>
        <input type="text" v-model="commentContent" style="width:700px">
        <button class="ms-3" style>댓글 작성</button>
      </form>
    </div>
    <div class="container mt-4 d-flex flex-column align-items-center">
      <h4 style="color:white" class="my-3">댓글</h4>
      <table style="text-align:center;" class="fs-6">
        <thead>
          <tr>
            <th>댓글</th>
            <th>작성자</th>
            <th>수정</th>
            <th>삭제</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comment in review.comments" :key="comment.id" :comment="comment">
            <td>{{ comment[0] }} </td>
            <td>{{ comment[1] }}</td>
            <td>
              <b-button v-b-modal.modal-1 variant="none"><img src="@/assets/update.png" width="30px" v-if="comment[1] === username"></b-button>
              <b-modal id="modal-1" title="댓글수정">
                <form @submit.prevent="UpdateComment(comment)">
                  <input type="text" v-model="newComment" :placeholder="comment[0]">
                  <button class="btn btn-primary btn-sm">수정하기</button>
                </form>
              </b-modal>
            </td>
            <td>
              <button class="btn btn-none" @click="CommentDelete(comment.id)"><img src="@/assets/delete.png" width="30px" v-if="comment[1] === username"></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import jwt_decode from 'jwt-decode'
export default {
  name:'ReviewDetail',
  data(){
    return{
      review:[],
      commentContent :'',
      newComment:'',
      nowUser : '',
      username: ''
    }
  },
  props:{
    isLogin:{
      type:Boolean,
    }
  },
  created(){
    axios({
      url:`http://127.0.0.1:8000/memovies/community/reviews/`+this.$route.params.reviewId,
      method:'get',
      headers: {
          Authorization: `JWT ${localStorage.getItem('jwt')}`,
        },
      })
      .then(res=>{
        this.review = res.data
        if (this.isLogin) {
          this.nowUser = jwt_decode(localStorage.getItem('jwt')).user_id
          this.username = jwt_decode(localStorage.getItem('jwt')).username
        }
      })
  },
  methods:{
    getReview: function(){
      axios({
        url:`http://127.0.0.1:8000/memovies/community/reviews/`+this.$route.params.reviewId,
        method:'get',
        headers: {
          Authorization: `JWT ${localStorage.getItem('jwt')}`,
        },
      })
        .then(res=>{
          this.review = res.data
          
        })
        .catch(err => {
          console.log(err)
        })
    },
    createComment(){
      axios({
        url:'http://127.0.0.1:8000/memovies/community/reviews/'+this.$route.params.reviewId+'/comments/',
        method:'post',
        headers: {
          Authorization: `JWT ${localStorage.getItem('jwt')}`,
        },
        data:{
          content: this.commentContent,
          review:this.$route.params.reviewId,
          user:this.nowUser,
        }
      })
        .then(res=>{
          console.log(res.data)
          this.commentContent = ''
          this.getReview()
        })
        .catch(err=>{
          console.log(err.response.data)
          alert('Login이 필요합니다!')
          this.$router.push({name:'Login'})
        })
    },
    CommentDelete(commentId){
      axios({
        url:`http://127.0.0.1:8000/memovies/community/comments/`+commentId,
        method:'delete',
        headers: {
          Authorization: `JWT ${localStorage.getItem('jwt')}`,
        }
      })
        .then(res=>{
          console.log(res)
          this.getReview()
        })
        .catch(err=>{
          console.log(err)
        })
    },
    UpdateComment(comment){
      // const username = jwt_decode(localStorage.getItem('jwt')).username
      // const userid = jwt_decode(localStorage.getItem('jwt')).user_id
      axios({
        url:`http://127.0.0.1:8000/memovies/community/comments/`+comment.id+'/',
        method:'put',
        headers: {
          Authorization: `JWT ${localStorage.getItem('jwt')}`,
        },
        data:{
          content:this.newComment,
          user:this.nowUser,
        }
      })
        .then(res=>{
          console.log(res)
          this.newComment =''
          this.getReview()
        })
        .catch(err=>{
          console.log(err)
        })
    },
    reviewDelete(reviewId){
        axios({
        url:`http://127.0.0.1:8000/memovies/community/reviews/`+reviewId+'/change/',
        method:'delete',
        headers: {
          Authorization: `JWT ${localStorage.getItem('jwt')}`,
        },
      })
        .then(res=>{
          console.log(res)
          this.$router.push({name:'Community'})
        })
        .catch(err=>{
          console.log(err)
        })
    },
    reviewUpdate(reviewId){
      this.$router.push({ name:'ReviewUpdate', params:{reviewid: reviewId}})
    }
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
  #comment{
    background-color:lightgrey;
    border: 3px solid black;
    color:black;
  }
</style>