<template>
  <div class="col-3 font-neodgm d-flex flex-column align-items-center" style="margin-left:80px;">
    <img :src="poster_path" alt="movie_poster" style="width:200px; height:200px;">
    <h5 class="mt-2 ms-2">{{movie.fields.rank}}위 : {{movie.fields.movie_title}}</h5>
  </div>
</template>

<script>
export default {
  name:'boxOfficeItem',
  props:{
    movie:{
      type:Object,
    }
  },
  computed:{
    poster_path(){
      return (this.movie.fields.poster_path)
    }
  },
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR&display=swap');
@import url('//cdn.jsdelivr.net/gh/Dalgona/neodgm-webfont@1.521/neodgm/style.css');
<link rel="stylesheet" href="//cdn.jsdelivr.net/gh/Dalgona/neodgm-webfont@1.521/neodgm/style.css">

.font-neodgm { 
  font-family: 'NeoDunggeunmo'; 
}

</style>