<template>
<!-- review index페이지에서 보여줄 개별 영화 list -->
    <li>{{ review.title }}</li>
</template>

<script>
export default {
  name:'ReviewListItem',
  props:{
    review:{
      type:Object,
    }
  },
}
</script>

<style>

</style>