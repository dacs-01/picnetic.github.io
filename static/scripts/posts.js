//tutorial used for grid layout: https://www.youtube.com/watch?v=MdKDHkhdCto&ab_channel=ConorBailey

// ~~~~~~~~~IMAGE SETUP~~~~~~~~~~~~~~~~~~
//array that will hold the post information pulled from database
const posts = [];


//images to just check homepage look and modal function
const images = [
    "static/images/campusphoto1.jpg",
    "static/images/normphoto1.jpg",
    "static/images/memephoto1.jpg",
    "static/images/sportsphoto1.jpg",
    "static/images/normphoto2.jpg",
    "static/images/stuorgphoto1.jpg",
    "static/images/memephoto2.jpg",
    "static/images/sportphoto3.jpg",
    "static/images/sportphoto2.jpg",
    "static/images/normphoto3.jpg",
    "static/images/normphoto4.jpg",
];

let imageIndex = 0;

for(let i = 0; i< 40; i++){
    let post = {
        //user: username 
        id: i, //this would eventually be the post ID that is given when a new post is created
        caption: `Post ${i}`,  //related caption (if one) 
        image: images[imageIndex] //would be the image related to that post ID but for now, it is the array above
        //likes: like Count
        //comments: comment Data
    }
    posts.push(post);
    imageIndex++;
    if(imageIndex > images.length -1) imageIndex = 0;
    
}
//testing
//console.log(posts);
