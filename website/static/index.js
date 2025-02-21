function like(post_id){
    const likeCount = document.getElementById(`like-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);


      fetch(`/like-post/${postId}`, {method : "POST"}).then(res)=>res.json().then
          
      })
    console.log(likeCount.value);
}   